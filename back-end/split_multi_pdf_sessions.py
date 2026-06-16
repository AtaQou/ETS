#!/usr/bin/env python3
"""Split sessions that accidentally contain translations from multiple PDFs.

The experiment app did not always rotate sessions on PDF upload/change. This
script repairs historical data by splitting affected sessions into contiguous
PDF segments, reassigning translation rows to new session IDs, and preserving
an audit table that records the original session mapping.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sqlite3
import uuid
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


ATHENS = ZoneInfo("Europe/Athens")


@dataclass
class Segment:
    doc_key: str
    doc_id: int | None
    doc_name: str
    events: list[sqlite3.Row]
    start_dt: datetime | None = None
    end_dt: datetime | None = None
    session_id: str | None = None
    start_source: str = ""
    output_mode: str = "on"
    translation_mode: str = "word"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--db",
        default=str(Path(__file__).resolve().parent / "ETSsqLiteDB"),
        help="Path to the SQLite DB.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply the split. Without this flag, only prints a dry-run report.",
    )
    parser.add_argument(
        "--backup-dir",
        default=str(Path(__file__).resolve().parent / "db_backups"),
        help="Directory for DB backups created before --apply.",
    )
    return parser.parse_args()


def parse_local(value: str | None) -> datetime | None:
    if not value:
        return None
    raw = str(value).strip().replace(" ", "T")
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=ATHENS)
    return parsed.astimezone(ATHENS)


def parse_event_time(value: str) -> datetime:
    raw = str(value).strip()
    if raw.endswith("Z"):
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    else:
        parsed = datetime.fromisoformat(raw)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=ATHENS)
    return parsed.astimezone(ATHENS)


def format_db_time(value: datetime | None) -> str | None:
    if value is None:
        return None
    local_value = value.astimezone(ATHENS).replace(tzinfo=None)
    if local_value.microsecond:
        return local_value.isoformat(timespec="milliseconds")
    return local_value.isoformat(timespec="seconds")


def now_for_audit() -> str:
    return datetime.now(ATHENS).replace(tzinfo=None).isoformat(timespec="seconds")


def to_json(payload: object) -> str | None:
    if payload is None:
        return None
    return json.dumps(payload, ensure_ascii=False)


def load_json(payload: str | None) -> object:
    if not payload:
        return None
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        return payload


def update_start_settings(
    payload: str | None,
    *,
    doc_name: str,
    output_mode: str,
    translation_mode: str,
) -> str | None:
    settings = load_json(payload)
    if not isinstance(settings, dict):
        return payload
    updated = {
        **settings,
        "currentPdfFile": doc_name or None,
        "translationOutputMode": output_mode or "on",
        "translationMode": translation_mode or "word",
    }
    return to_json(updated)


def ensure_schema(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(user_sessions)")
    columns = {row[1] for row in cursor.fetchall()}
    additions = {
        "splitFromSessionID": "TEXT",
        "splitSegmentIndex": "INTEGER",
        "splitSegmentCount": "INTEGER",
        "splitNote": "TEXT",
    }
    for column, column_type in additions.items():
        if column not in columns:
            cursor.execute(f"ALTER TABLE user_sessions ADD COLUMN {column} {column_type}")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS session_split_audit (
            splitID INTEGER PRIMARY KEY AUTOINCREMENT,
            originalSessionID TEXT NOT NULL,
            newSessionID TEXT NOT NULL,
            userID INTEGER NOT NULL,
            docID INTEGER,
            docName TEXT,
            segmentIndex INTEGER NOT NULL,
            segmentCount INTEGER NOT NULL,
            originalStartedAt DATETIME,
            originalEndedAt DATETIME,
            newStartedAt DATETIME,
            newEndedAt DATETIME,
            startSource TEXT,
            translationCount INTEGER NOT NULL,
            translationOutputMode TEXT,
            translationMode TEXT,
            createdAt DATETIME NOT NULL
        )
        """
    )


def doc_key(row: sqlite3.Row) -> str:
    if row["docID"] is not None:
        return f"id:{row['docID']}"
    doc_name = (row["docName"] or "").strip()
    if doc_name:
        return f"name:{doc_name}"
    return "unknown"


def build_segments(events: list[sqlite3.Row]) -> list[Segment]:
    segments: list[Segment] = []
    current: Segment | None = None

    for event in events:
        key = doc_key(event)
        doc_name = (event["docName"] or "").strip()
        if current is None or current.doc_key != key:
            current = Segment(
                doc_key=key,
                doc_id=event["docID"],
                doc_name=doc_name,
                events=[],
            )
            segments.append(current)
        current.events.append(event)

    for segment in segments:
        first = segment.events[0]
        last = segment.events[-1]
        segment.end_dt = parse_event_time(last["translatedAt"])
        segment.output_mode = (first["translationOutputMode"] or "on").strip().lower() or "on"
        segment.translation_mode = (first["translationMode"] or "word").strip().lower() or "word"

    return segments


def pick_segment_start(
    conn: sqlite3.Connection,
    *,
    user_id: int,
    original_start: datetime | None,
    original_end: datetime | None,
    previous_segment_end: datetime | None,
    segment: Segment,
    segment_index: int,
) -> tuple[datetime | None, str]:
    first_translation = parse_event_time(segment.events[0]["translatedAt"])
    if segment_index == 0:
        return original_start or first_translation, "original_session_start"

    upload_dt = None
    if segment.doc_id is not None:
        row = conn.execute(
            "SELECT uploadDate FROM documents WHERE userID = ? AND docID = ?",
            (user_id, segment.doc_id),
        ).fetchone()
        if row:
            upload_dt = parse_local(row["uploadDate"])

    if upload_dt and original_start and original_end:
        within_original = original_start <= upload_dt <= original_end
        after_previous = previous_segment_end is None or upload_dt >= previous_segment_end
        before_first_translation = upload_dt <= first_translation
        if within_original and after_previous and before_first_translation:
            return upload_dt, "document_upload_time"

    return first_translation, "first_translation_time"


def fetch_multi_pdf_sessions(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(
        """
        WITH docs AS (
            SELECT
                sessionID,
                COUNT(DISTINCT COALESCE(NULLIF(TRIM(docName), ''), CAST(docID AS TEXT))) AS docCount
            FROM translation_events
            GROUP BY sessionID
        )
        SELECT s.*
        FROM user_sessions s
        JOIN docs ON docs.sessionID = s.sessionID
        WHERE docs.docCount > 1
        ORDER BY s.userID, s.startedAt, s.sessionID
        """
    ).fetchall()


def split_session(conn: sqlite3.Connection, session: sqlite3.Row, *, dry_run: bool) -> list[Segment]:
    events = conn.execute(
        """
        SELECT
            eventID, userID, sessionID, docID, docName, sourceText, translatedText,
            targetLang, translationMode, translatedAt,
            COALESCE(translationOutputMode, 'on') AS translationOutputMode
        FROM translation_events
        WHERE sessionID = ?
        ORDER BY translatedAt ASC, eventID ASC
        """,
        (session["sessionID"],),
    ).fetchall()
    segments = build_segments(events)
    if len(segments) <= 1:
        return segments

    original_start = parse_local(session["startedAt"])
    original_end = parse_local(session["endedAt"])
    original_session_id = session["sessionID"]

    for index, segment in enumerate(segments):
        previous_end = segments[index - 1].end_dt if index > 0 else None
        segment.start_dt, segment.start_source = pick_segment_start(
            conn,
            user_id=session["userID"],
            original_start=original_start,
            original_end=original_end,
            previous_segment_end=previous_end,
            segment=segment,
            segment_index=index,
        )
        segment.session_id = original_session_id if index == 0 else str(uuid.uuid4())

    if dry_run:
        return segments

    created_at = now_for_audit()
    segment_count = len(segments)
    for index, segment in enumerate(segments):
        segment_number = index + 1
        note = (
            f"This session was split during experiment analysis from original session "
            f"{original_session_id}. Segment {segment_number}/{segment_count} contains "
            f"{segment.doc_name or 'unknown PDF'}; timestamps were reconstructed from "
            f"{segment.start_source.replace('_', ' ')} and last translated word."
        )
        start_settings = update_start_settings(
            session["startSettings"],
            doc_name=segment.doc_name,
            output_mode=segment.output_mode,
            translation_mode=segment.translation_mode,
        )
        end_reason = session["endReason"] if index == segment_count - 1 else "split_document_changed"

        if index == 0:
            conn.execute(
                """
                UPDATE user_sessions
                SET startedAt = ?, endedAt = ?, endReason = ?, startSettings = ?,
                    splitFromSessionID = ?, splitSegmentIndex = ?,
                    splitSegmentCount = ?, splitNote = ?
                WHERE sessionID = ?
                """,
                (
                    format_db_time(segment.start_dt),
                    format_db_time(segment.end_dt),
                    end_reason,
                    start_settings,
                    original_session_id,
                    segment_number,
                    segment_count,
                    note,
                    original_session_id,
                ),
            )
        else:
            conn.execute(
                """
                INSERT INTO user_sessions (
                    sessionID, userID, trackerAddress, trackerName, startedAt, endedAt,
                    startSettings, endReason, splitFromSessionID, splitSegmentIndex,
                    splitSegmentCount, splitNote
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    segment.session_id,
                    session["userID"],
                    session["trackerAddress"],
                    session["trackerName"],
                    format_db_time(segment.start_dt),
                    format_db_time(segment.end_dt),
                    start_settings,
                    end_reason,
                    original_session_id,
                    segment_number,
                    segment_count,
                    note,
                ),
            )
            event_ids = [event["eventID"] for event in segment.events]
            conn.executemany(
                "UPDATE translation_events SET sessionID = ? WHERE eventID = ?",
                [(segment.session_id, event_id) for event_id in event_ids],
            )

        conn.execute(
            """
            INSERT INTO session_split_audit (
                originalSessionID, newSessionID, userID, docID, docName,
                segmentIndex, segmentCount, originalStartedAt, originalEndedAt,
                newStartedAt, newEndedAt, startSource, translationCount,
                translationOutputMode, translationMode, createdAt
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                original_session_id,
                segment.session_id,
                session["userID"],
                segment.doc_id,
                segment.doc_name,
                segment_number,
                segment_count,
                session["startedAt"],
                session["endedAt"],
                format_db_time(segment.start_dt),
                format_db_time(segment.end_dt),
                segment.start_source,
                len(segment.events),
                segment.output_mode,
                segment.translation_mode,
                created_at,
            ),
        )

    reassign_settings_changes(conn, session, segments)
    rebuild_translation_stats(conn, [segment.session_id for segment in segments if segment.session_id])
    return segments


def reassign_settings_changes(
    conn: sqlite3.Connection,
    session: sqlite3.Row,
    segments: list[Segment],
) -> None:
    changes = conn.execute(
        "SELECT changeID, changedAt FROM settings_change_events WHERE sessionID = ?",
        (session["sessionID"],),
    ).fetchall()
    if not changes:
        return

    for change in changes:
        changed_at = parse_local(change["changedAt"])
        target_session_id = segments[-1].session_id
        if changed_at:
            for segment in segments:
                if segment.start_dt and segment.end_dt and segment.start_dt <= changed_at <= segment.end_dt:
                    target_session_id = segment.session_id
                    break
                if segment.start_dt and changed_at >= segment.start_dt:
                    target_session_id = segment.session_id
        if target_session_id != session["sessionID"]:
            conn.execute(
                "UPDATE settings_change_events SET sessionID = ? WHERE changeID = ?",
                (target_session_id, change["changeID"]),
            )


def rebuild_translation_stats(conn: sqlite3.Connection, session_ids: list[str]) -> None:
    if not session_ids:
        return
    conn.executemany(
        "DELETE FROM translation_stats WHERE sessionID = ?",
        [(session_id,) for session_id in session_ids],
    )
    placeholders = ",".join("?" for _ in session_ids)
    events = conn.execute(
        f"""
        SELECT
            userID, sessionID, sourceText, targetLang, translationMode,
            translatedText, translatedAt, eventID
        FROM translation_events
        WHERE sessionID IN ({placeholders})
        ORDER BY translatedAt ASC, eventID ASC
        """,
        session_ids,
    ).fetchall()

    grouped: dict[tuple[object, ...], list[sqlite3.Row]] = defaultdict(list)
    for event in events:
        key = (
            event["userID"],
            event["sessionID"],
            event["sourceText"],
            event["targetLang"],
            event["translationMode"],
        )
        grouped[key].append(event)

    rows = []
    for key, key_events in grouped.items():
        last_event = key_events[-1]
        rows.append((*key, len(key_events), last_event["translatedText"], last_event["translatedAt"]))

    conn.executemany(
        """
        INSERT INTO translation_stats (
            userID, sessionID, sourceText, targetLang, translationMode,
            usageCount, lastTranslation, lastTranslatedAt
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )


def create_backup(db_path: Path, backup_dir: Path) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"{db_path.name}.before_split_{stamp}"
    shutil.copy2(db_path, backup_path)
    return backup_path


def main() -> None:
    args = parse_args()
    db_path = Path(args.db)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    try:
        ensure_schema(conn)
        sessions = fetch_multi_pdf_sessions(conn)
        print(f"Multi-PDF sessions found: {len(sessions)}")
        if not args.apply:
            print("Dry run only. Re-run with --apply to modify the DB.")

        backup_path = None
        if args.apply and sessions:
            backup_path = create_backup(db_path, Path(args.backup_dir))
            print(f"Backup created: {backup_path}")

        total_new_sessions = 0
        for session in sessions:
            segments = split_session(conn, session, dry_run=not args.apply)
            if len(segments) <= 1:
                continue
            total_new_sessions += len(segments) - 1
            print(
                f"{session['userID']} {session['sessionID']} -> "
                f"{len(segments)} segments"
            )
            for index, segment in enumerate(segments, start=1):
                print(
                    "  "
                    f"{index}/{len(segments)} "
                    f"{segment.doc_name or 'unknown PDF'} "
                    f"{format_db_time(segment.start_dt)} -> {format_db_time(segment.end_dt)} "
                    f"events={len(segment.events)} "
                    f"output={segment.output_mode} "
                    f"startSource={segment.start_source}"
                )

        if args.apply:
            conn.commit()
            remaining = fetch_multi_pdf_sessions(conn)
            print(f"New sessions inserted: {total_new_sessions}")
            print(f"Remaining multi-PDF sessions: {len(remaining)}")
        else:
            conn.rollback()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
