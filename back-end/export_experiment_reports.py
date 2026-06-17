import argparse
import csv
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export ETS experiment data to CSV files."
    )
    parser.add_argument(
        "--db-path",
        default=str(Path(__file__).resolve().parent / "ETSsqLiteDB"),
        help="Path to SQLite database file.",
    )
    parser.add_argument(
        "--user-id",
        type=int,
        default=None,
        help="Filter exports by userID.",
    )
    parser.add_argument(
        "--session-id",
        default=None,
        help="Filter exports by sessionID.",
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Output directory for CSV files. Defaults to back-end/experiment_reports/<timestamp>.",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include sessions marked as hidden. By default hidden sessions are excluded from exports.",
    )
    return parser.parse_args()


def _json_to_string(value: Any) -> Any:
    if value is None:
        return value
    if not isinstance(value, str):
        return value
    try:
        parsed = json.loads(value)
        return json.dumps(parsed, ensure_ascii=False, sort_keys=True)
    except json.JSONDecodeError:
        return value


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _fetch_all(
    conn: sqlite3.Connection, query: str, params: tuple[Any, ...]
) -> list[dict[str, Any]]:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    return [dict(row) for row in cursor.fetchall()]


def ensure_tables(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_sessions
        ([sessionID] TEXT PRIMARY KEY, [userID] INTEGER NOT NULL, [trackerAddress] TEXT, [trackerName] TEXT,
         [startedAt] DATETIME NOT NULL, [endedAt] DATETIME, [startSettings] TEXT, [endReason] TEXT,
         [isHidden] INTEGER NOT NULL DEFAULT 0, [hiddenAt] DATETIME, [hiddenByUserID] INTEGER, [hiddenReason] TEXT)
        """
    )
    cursor.execute("PRAGMA table_info(user_sessions)")
    session_columns = {row[1] for row in cursor.fetchall()}
    if "isHidden" not in session_columns:
        cursor.execute("ALTER TABLE user_sessions ADD COLUMN isHidden INTEGER NOT NULL DEFAULT 0")
    if "hiddenAt" not in session_columns:
        cursor.execute("ALTER TABLE user_sessions ADD COLUMN hiddenAt DATETIME")
    if "hiddenByUserID" not in session_columns:
        cursor.execute("ALTER TABLE user_sessions ADD COLUMN hiddenByUserID INTEGER")
    if "hiddenReason" not in session_columns:
        cursor.execute("ALTER TABLE user_sessions ADD COLUMN hiddenReason TEXT")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS translation_events
        ([eventID] INTEGER PRIMARY KEY AUTOINCREMENT, [userID] INTEGER NOT NULL, [sessionID] TEXT NOT NULL,
         [docID] INTEGER, [page] INTEGER, [sourceText] TEXT NOT NULL, [translatedText] TEXT NOT NULL,
         [sourceLang] TEXT DEFAULT 'en', [targetLang] TEXT NOT NULL, [translationMode] TEXT DEFAULT 'word',
         [provider] TEXT DEFAULT 'google', [translatedAt] DATETIME NOT NULL, [settingsSnapshot] TEXT)
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS translation_stats
        ([userID] INTEGER NOT NULL, [sessionID] TEXT NOT NULL, [sourceText] TEXT NOT NULL,
         [targetLang] TEXT NOT NULL, [translationMode] TEXT NOT NULL, [usageCount] INTEGER NOT NULL DEFAULT 1,
         [lastTranslation] TEXT, [lastTranslatedAt] DATETIME NOT NULL,
         PRIMARY KEY (userID, sessionID, sourceText, targetLang, translationMode))
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS settings_change_events
        ([changeID] INTEGER PRIMARY KEY AUTOINCREMENT, [userID] INTEGER NOT NULL, [sessionID] TEXT,
         [changedFields] TEXT NOT NULL, [oldSettings] TEXT, [newSettings] TEXT NOT NULL, [changedAt] DATETIME NOT NULL)
        """
    )
    conn.commit()


def build_output_dir(args: argparse.Namespace) -> Path:
    if args.out_dir:
        out_dir = Path(args.out_dir).expanduser().resolve()
    else:
        base_dir = Path(__file__).resolve().parent / "experiment_reports"
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        scope = []
        if args.user_id is not None:
            scope.append(f"user{args.user_id}")
        if args.session_id:
            scope.append(f"session_{args.session_id}")
        suffix = "_" + "_".join(scope) if scope else ""
        out_dir = base_dir / f"{stamp}{suffix}"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def export_data(
    db_path: str, out_dir: Path, user_id: int | None, session_id: str | None, include_hidden: bool
) -> dict[str, int]:
    params: list[Any] = []
    where_events = ["1 = 1"]
    where_sessions = ["1 = 1"]

    if user_id is not None:
        where_events.append("e.userID = ?")
        where_sessions.append("s.userID = ?")
        params.append(user_id)

    session_params: list[Any] = params.copy()
    event_params: list[Any] = params.copy()

    if session_id:
        where_events.append("e.sessionID = ?")
        where_sessions.append("s.sessionID = ?")
        event_params.append(session_id)
        session_params.append(session_id)

    if not include_hidden:
        where_events.append("COALESCE(s.isHidden, 0) = 0")
        where_sessions.append("COALESCE(s.isHidden, 0) = 0")

    where_events_sql = " AND ".join(where_events)
    where_sessions_sql = " AND ".join(where_sessions)

    conn = sqlite3.connect(db_path)
    try:
        ensure_tables(conn)

        sessions_query = f"""
            SELECT
                s.sessionID, s.userID, u.username, s.trackerAddress, s.trackerName,
                s.startedAt, s.endedAt, s.endReason, s.startSettings,
                COALESCE(s.isHidden, 0) AS isHidden, s.hiddenAt, s.hiddenByUserID, s.hiddenReason,
                COALESCE(te.translationCount, 0) AS translationCount,
                COALESCE(sc.settingsChangeCount, 0) AS settingsChangeCount
            FROM user_sessions s
            LEFT JOIN users u ON u.userID = s.userID
            LEFT JOIN (
                SELECT sessionID, COUNT(*) AS translationCount
                FROM translation_events
                GROUP BY sessionID
            ) te ON te.sessionID = s.sessionID
            LEFT JOIN (
                SELECT sessionID, COUNT(*) AS settingsChangeCount
                FROM settings_change_events
                GROUP BY sessionID
            ) sc ON sc.sessionID = s.sessionID
            WHERE {where_sessions_sql}
            ORDER BY s.startedAt DESC
        """
        sessions = _fetch_all(conn, sessions_query, tuple(session_params))
        for row in sessions:
            row["startSettings"] = _json_to_string(row.get("startSettings"))

        translations_query = f"""
            SELECT
                e.eventID, e.userID, u.username, e.sessionID, e.docID, e.page,
                e.sourceText, e.translatedText, e.sourceLang, e.targetLang,
                e.translationMode, e.provider, e.translatedAt, e.settingsSnapshot
            FROM translation_events e
            LEFT JOIN users u ON u.userID = e.userID
            LEFT JOIN user_sessions s ON s.sessionID = e.sessionID
            WHERE {where_events_sql}
            ORDER BY e.translatedAt DESC
        """
        translations = _fetch_all(conn, translations_query, tuple(event_params))
        for row in translations:
            row["settingsSnapshot"] = _json_to_string(row.get("settingsSnapshot"))

        settings_changes_query = f"""
            SELECT
                c.changeID, c.userID, u.username, c.sessionID, c.changedFields,
                c.oldSettings, c.newSettings, c.changedAt
            FROM settings_change_events c
            LEFT JOIN users u ON u.userID = c.userID
            LEFT JOIN user_sessions s ON s.sessionID = c.sessionID
            WHERE {" AND ".join(where_events).replace("e.", "c.")}
            ORDER BY c.changedAt DESC
        """
        settings_changes = _fetch_all(
            conn, settings_changes_query, tuple(event_params)
        )
        for row in settings_changes:
            row["changedFields"] = _json_to_string(row.get("changedFields"))
            row["oldSettings"] = _json_to_string(row.get("oldSettings"))
            row["newSettings"] = _json_to_string(row.get("newSettings"))

        stats_query = f"""
            SELECT
                ts.userID, u.username, ts.sessionID, ts.sourceText, ts.targetLang,
                ts.translationMode, ts.usageCount, ts.lastTranslation, ts.lastTranslatedAt
            FROM translation_stats ts
            LEFT JOIN users u ON u.userID = ts.userID
            LEFT JOIN user_sessions s ON s.sessionID = ts.sessionID
            WHERE {" AND ".join(where_events).replace("e.", "ts.")}
            ORDER BY ts.lastTranslatedAt DESC
        """
        stats = _fetch_all(conn, stats_query, tuple(event_params))
    finally:
        conn.close()

    _write_csv(
        out_dir / "sessions.csv",
        sessions,
        [
            "sessionID",
            "userID",
            "username",
            "trackerAddress",
            "trackerName",
            "startedAt",
            "endedAt",
            "endReason",
            "startSettings",
            "isHidden",
            "hiddenAt",
            "hiddenByUserID",
            "hiddenReason",
            "translationCount",
            "settingsChangeCount",
        ],
    )
    _write_csv(
        out_dir / "translation_events.csv",
        translations,
        [
            "eventID",
            "userID",
            "username",
            "sessionID",
            "docID",
            "page",
            "sourceText",
            "translatedText",
            "sourceLang",
            "targetLang",
            "translationMode",
            "provider",
            "translatedAt",
            "settingsSnapshot",
        ],
    )
    _write_csv(
        out_dir / "settings_changes.csv",
        settings_changes,
        [
            "changeID",
            "userID",
            "username",
            "sessionID",
            "changedFields",
            "oldSettings",
            "newSettings",
            "changedAt",
        ],
    )
    _write_csv(
        out_dir / "translation_stats.csv",
        stats,
        [
            "userID",
            "username",
            "sessionID",
            "sourceText",
            "targetLang",
            "translationMode",
            "usageCount",
            "lastTranslation",
            "lastTranslatedAt",
        ],
    )

    return {
        "sessions": len(sessions),
        "translation_events": len(translations),
        "settings_changes": len(settings_changes),
        "translation_stats": len(stats),
    }


def main() -> None:
    args = parse_args()
    out_dir = build_output_dir(args)
    counts = export_data(args.db_path, out_dir, args.user_id, args.session_id, args.include_hidden)

    print(f"Export completed: {out_dir}")
    print(f"sessions.csv rows: {counts['sessions']}")
    print(f"translation_events.csv rows: {counts['translation_events']}")
    print(f"settings_changes.csv rows: {counts['settings_changes']}")
    print(f"translation_stats.csv rows: {counts['translation_stats']}")


if __name__ == "__main__":
    main()
