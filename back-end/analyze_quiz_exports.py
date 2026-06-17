#!/usr/bin/env python3
from __future__ import annotations

import csv
import io
import json
import math
import re
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from statistics import median
from zipfile import ZipFile

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "ETSsqLiteDB"
EXPORT_DIR = BASE_DIR / "quiz_exports"
REPORT_PATH = BASE_DIR / "quiz_analysis_report.md"
JOINED_CSV = BASE_DIR / "quiz_analysis_joined.csv"
USER_SUMMARY_CSV = BASE_DIR / "quiz_analysis_user_summary.csv"
SUS_PAIRED_CSV = BASE_DIR / "quiz_analysis_sus_paired.csv"
QUESTION_STATS_CSV = BASE_DIR / "quiz_analysis_question_stats.csv"
MISSING_SESSION_REVIEW_CSV = BASE_DIR / "quiz_analysis_missing_session_review.csv"
PDF_CONDITION_COMPARISON_CSV = BASE_DIR / "quiz_analysis_pdf_condition_comparison.csv"

TEXT_DOC_RE = re.compile(r"^(b2|c1|c2)[_:_-]", re.I)
SCORE_RE = re.compile(r"(-?\d+(?:\.\d+)?)\s*/\s*(-?\d+(?:\.\d+)?)")
NUMBER_RE = re.compile(r"-?\d+(?:\.\d+)?")

DOC_MAP = [
    ("animals", "b2_animals_of_rainforests_1.pdf"),
    ("electromagnetic", "b2_electromagnetic_radiation_2.pdf"),
    ("sticky", "b2_sticky_fingers_4.pdf"),
    ("first american", "b2_first_american_3.pdf"),
    ("native american", "c1_native_american_conflicts_3.pdf"),
    ("age of exploration", "c1_age_of_exploration_1.pdf"),
    ("worldwide loss of bees", "c1_bee_reading_2.pdf"),
    ("bees", "c1_bee_reading_2.pdf"),
    ("walt disney", "c1_walt_disney_4.pdf"),
    ("noisy humans", "c2_noisy_humans_1.pdf"),
    ("rosa parks", "c2_rosa_parks_2.pdf"),
]

LEVEL_ORDER = {"b2": 0, "c1": 1, "c2": 2}


def decode_csv_from_zip(path: Path) -> tuple[str, str]:
    with ZipFile(path) as zf:
        members = [m for m in zf.namelist() if not m.endswith("/")]
        if not members:
            raise ValueError(f"No files in {path}")
        name = members[0]
        data = zf.read(name)
    for encoding in ("utf-8-sig", "utf-16", "latin-1"):
        try:
            return name, data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return name, data.decode("utf-8", errors="replace")


def read_zip_csv(path: Path) -> tuple[str, list[dict[str, str]], list[str]]:
    member, text = decode_csv_from_zip(path)
    reader = csv.DictReader(io.StringIO(text))
    rows = list(reader)
    return member, rows, reader.fieldnames or []


def clean_text(value: object) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def shorten_text(value: object, limit: int) -> str:
    text = clean_text(value)
    if len(text) <= limit:
        return text
    shortened = text[: max(0, limit - 3)].rsplit(" ", 1)[0]
    return (shortened or text[: max(0, limit - 3)]) + "..."


def parse_score(value: object) -> tuple[float | None, float | None]:
    text = clean_text(value)
    if not text:
        return None, None
    match = SCORE_RE.search(text)
    if match:
        return float(match.group(1)), float(match.group(2))
    nums = NUMBER_RE.findall(text)
    if len(nums) == 1:
        return float(nums[0]), None
    return None, None


def parse_likert(value: object) -> int | None:
    nums = NUMBER_RE.findall(clean_text(value))
    if not nums:
        return None
    return int(float(nums[0]))


def parse_google_timestamp(value: object) -> datetime | None:
    text = clean_text(value)
    if not text:
        return None
    text = text.replace("π.μ.", "AM").replace("μ.μ.", "PM")
    text = text.replace("πμ", "AM").replace("μμ", "PM")
    text = re.sub(r"\s+GMT[+-]\d+", "", text)
    for fmt in ("%Y/%m/%d %I:%M:%S %p", "%Y/%m/%d %H:%M:%S"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    return None


def parse_iso(value: object) -> datetime | None:
    text = clean_text(value)
    if not text:
        return None
    raw = text.replace(" ", "T")
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if dt.tzinfo is not None:
        # DB session times are Athens local naive. Google exported GMT+3, so convert UTC event
        # timestamps to the same local clock for interval comparisons.
        dt = dt.astimezone().replace(tzinfo=None)
    return dt


def minutes_between(start: object, end: object) -> float | None:
    s = parse_iso(start)
    e = parse_iso(end)
    if not s or not e:
        return None
    return round((e - s).total_seconds() / 60, 2)


def safe_float(value: object) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def mean(values: list[float]) -> float | None:
    vals = [v for v in values if v is not None and not math.isnan(v)]
    if not vals:
        return None
    return sum(vals) / len(vals)


def sd(values: list[float]) -> float | None:
    vals = [v for v in values if v is not None and not math.isnan(v)]
    if len(vals) < 2:
        return None
    m = sum(vals) / len(vals)
    return math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))


def summarize(values: list[float]) -> dict[str, float | int | None]:
    vals = sorted(v for v in values if v is not None and not math.isnan(v))
    if not vals:
        return {"n": 0, "mean": None, "median": None, "sd": None, "min": None, "max": None}
    return {
        "n": len(vals),
        "mean": sum(vals) / len(vals),
        "median": median(vals),
        "sd": sd(vals),
        "min": vals[0],
        "max": vals[-1],
    }


def fmt_num(value: object, digits: int = 2) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        if math.isnan(value):
            return "-"
        return f"{value:.{digits}f}"
    return str(value)


def fmt_summary(stats: dict[str, object]) -> str:
    return f"n={stats['n']}, mean={fmt_num(stats['mean'])}, median={fmt_num(stats['median'])}, sd={fmt_num(stats['sd'])}, range={fmt_num(stats['min'])}-{fmt_num(stats['max'])}"


def fmt_summary_el(stats: dict[str, object]) -> str:
    return f"n={stats['n']}, μέσος={fmt_num(stats['mean'])}, διάμεσος={fmt_num(stats['median'])}, ΤΑ={fmt_num(stats['sd'])}, εύρος={fmt_num(stats['min'])}-{fmt_num(stats['max'])}"


def rankdata(values: list[float]) -> list[float]:
    indexed = sorted((v, i) for i, v in enumerate(values))
    ranks = [0.0] * len(values)
    pos = 0
    while pos < len(indexed):
        end = pos + 1
        while end < len(indexed) and indexed[end][0] == indexed[pos][0]:
            end += 1
        avg_rank = (pos + 1 + end) / 2
        for _, original_idx in indexed[pos:end]:
            ranks[original_idx] = avg_rank
        pos = end
    return ranks


def pearson(xs: list[float], ys: list[float]) -> float | None:
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(pairs) < 3:
        return None
    xvals = [p[0] for p in pairs]
    yvals = [p[1] for p in pairs]
    mx = sum(xvals) / len(xvals)
    my = sum(yvals) / len(yvals)
    denom_x = math.sqrt(sum((x - mx) ** 2 for x in xvals))
    denom_y = math.sqrt(sum((y - my) ** 2 for y in yvals))
    if denom_x == 0 or denom_y == 0:
        return None
    return sum((x - mx) * (y - my) for x, y in pairs) / (denom_x * denom_y)


def spearman(xs: list[float], ys: list[float]) -> float | None:
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(pairs) < 3:
        return None
    return pearson(rankdata([p[0] for p in pairs]), rankdata([p[1] for p in pairs]))


def pooled_d(a: list[float], b: list[float]) -> float | None:
    if len(a) < 2 or len(b) < 2:
        return None
    sda = sd(a)
    sdb = sd(b)
    if not sda or not sdb:
        return None
    pooled = math.sqrt(((len(a) - 1) * sda**2 + (len(b) - 1) * sdb**2) / (len(a) + len(b) - 2))
    if pooled == 0:
        return None
    return ((mean(a) or 0) - (mean(b) or 0)) / pooled


def paired_d(diffs: list[float]) -> float | None:
    if len(diffs) < 2:
        return None
    s = sd(diffs)
    if not s:
        return None
    return (mean(diffs) or 0) / s


def level_for_doc(doc: str) -> str:
    match = TEXT_DOC_RE.match(doc or "")
    return match.group(1).lower() if match else "unknown"


def infer_doc_name(path: Path, member_name: str) -> str | None:
    text = f"{path.stem} {member_name}".lower().replace("_", " ")
    for needle, doc in DOC_MAP:
        if needle in text:
            return doc
    return None


def normalize_user_id(raw: object, session_usernames: set[str], all_usernames: set[str]) -> str:
    value = clean_text(raw)
    if not value:
        return ""
    value = value.replace("–", "-").replace("—", "-")
    value = re.sub(r"\s+", " ", value)

    # Google Form suffixes used for second SUS submissions, e.g. "1108367 2" or "1108382-2".
    suffix_match = re.match(r"^(.+?)[\s-]+([12])$", value)
    if suffix_match:
        base = clean_text(suffix_match.group(1))
    else:
        base = value

    if base in session_usernames:
        return base
    if base in all_usernames:
        # Special case in this DB: 1112119 exists but has no experiment sessions; 1112119c does.
        c_variant = f"{base}c"
        if c_variant in session_usernames:
            return c_variant
        return base
    c_variant = f"{base}c"
    if c_variant in session_usernames:
        return c_variant

    # If someone typed an appended suffix without a separator, only use it when the full
    # value is not a known user and the shortened value is known.
    for suffix in ("1", "2"):
        if base.endswith(suffix):
            shortened = base[: -len(suffix)]
            if shortened in session_usernames:
                return shortened
            if f"{shortened}c" in session_usernames:
                return f"{shortened}c"
    return base


def id_column(headers: list[str]) -> str | None:
    for header in headers:
        h = clean_text(header).lower().rstrip(":")
        if h == "id":
            return header
    for header in headers:
        h = clean_text(header).lower()
        if h.startswith("id") and "βαθ" not in h and "σχ" not in h:
            return header
    return None


def score_columns(headers: list[str]) -> list[str]:
    cols = []
    for header in headers:
        h = clean_text(header).lower()
        if "[βαθμολογία]" in h and not h.startswith("id"):
            cols.append(header)
    return cols


def ensure_analysis_schema(conn: sqlite3.Connection) -> None:
    session_columns = {row["name"] for row in conn.execute("PRAGMA table_info(user_sessions)").fetchall()}
    if "isHidden" not in session_columns:
        conn.execute("ALTER TABLE user_sessions ADD COLUMN isHidden INTEGER NOT NULL DEFAULT 0")
    if "hiddenAt" not in session_columns:
        conn.execute("ALTER TABLE user_sessions ADD COLUMN hiddenAt DATETIME")
    if "hiddenByUserID" not in session_columns:
        conn.execute("ALTER TABLE user_sessions ADD COLUMN hiddenByUserID INTEGER")
    if "hiddenReason" not in session_columns:
        conn.execute("ALTER TABLE user_sessions ADD COLUMN hiddenReason TEXT")
    conn.commit()


def get_db_users(conn: sqlite3.Connection) -> tuple[dict[str, int], set[str], set[str]]:
    rows = conn.execute("SELECT userID, username FROM users").fetchall()
    username_to_id = {str(r["username"]): r["userID"] for r in rows}
    session_rows = conn.execute(
        """
        SELECT DISTINCT u.username
        FROM users u
        JOIN user_sessions s ON s.userID = u.userID
        WHERE COALESCE(s.isHidden, 0) = 0
        """
    ).fetchall()
    session_usernames = {str(r["username"]) for r in session_rows}
    return username_to_id, set(username_to_id), session_usernames


def load_sessions(conn: sqlite3.Connection) -> tuple[list[dict[str, object]], dict[tuple[str, str], list[dict[str, object]]]]:
    rows = conn.execute(
        """
        SELECT s.sessionID, s.userID, u.username, s.trackerAddress, s.trackerName,
               s.startedAt, s.endedAt, s.endReason, s.startSettings,
               e.docID, e.docName,
               COUNT(*) AS translations,
               COUNT(DISTINCT e.sourceText) AS uniqueSourceWords,
               SUM(CASE WHEN e.isUndesired = 1 THEN 1 ELSE 0 END) AS undesiredEvents,
               MIN(e.translatedAt) AS firstTranslation,
               MAX(e.translatedAt) AS lastTranslation
        FROM user_sessions s
        JOIN users u ON u.userID = s.userID
        JOIN translation_events e ON e.sessionID = s.sessionID
        WHERE COALESCE(s.isHidden, 0) = 0
          AND (
            lower(e.docName) GLOB 'b2_*'
            OR lower(e.docName) GLOB 'c1_*'
            OR lower(e.docName) GLOB 'c2_*'
          )
        GROUP BY s.sessionID, e.docID, e.docName
        """
    ).fetchall()

    gap_rows = conn.execute(
        """
        SELECT e.sessionID, e.docName, e.translatedAt, COALESCE(e.translationOutputMode, 'on') AS outputMode
        FROM translation_events e
        JOIN user_sessions s ON s.sessionID = e.sessionID
        WHERE COALESCE(s.isHidden, 0) = 0
          AND (
            lower(e.docName) GLOB 'b2_*'
            OR lower(e.docName) GLOB 'c1_*'
            OR lower(e.docName) GLOB 'c2_*'
          )
        ORDER BY e.sessionID, e.docName, e.translatedAt, e.eventID
        """
    ).fetchall()
    gaps: dict[tuple[str, str], float] = defaultdict(float)
    mode_sequences: dict[tuple[str, str], list[str]] = defaultdict(list)
    previous_by_session_doc: dict[tuple[str, str], datetime] = {}
    for row in gap_rows:
        sid = row["sessionID"]
        doc = row["docName"] or ""
        key = (sid, doc)
        mode_sequences[key].append(row["outputMode"] or "on")
        dt = parse_iso(row["translatedAt"])
        if not dt:
            continue
        prev = previous_by_session_doc.get(key)
        if prev:
            gap = max(0.0, (dt - prev).total_seconds())
            if gap > gaps[key]:
                gaps[key] = gap
        previous_by_session_doc[key] = dt

    sessions = []
    for row in rows:
        item = dict(row)
        session_doc_key = (item["sessionID"], item.get("docName") or "")
        start_settings = {}
        try:
            start_settings = json.loads(item.get("startSettings") or "{}")
        except json.JSONDecodeError:
            start_settings = {}
        output_sequence = mode_sequences.get(session_doc_key, [])
        output_counts = Counter(output_sequence)
        output_counts.pop("", None)
        dominant_output_mode = output_counts.most_common(1)[0][0] if output_counts else clean_text(start_settings.get("translationOutputMode")) or "on"
        first_output_mode = output_sequence[0] if output_sequence else dominant_output_mode
        final_output_mode = output_sequence[-1] if output_sequence else dominant_output_mode
        mode_switch_count = sum(1 for a, b in zip(output_sequence, output_sequence[1:]) if a != b)
        output_mode = final_output_mode if mode_switch_count else dominant_output_mode
        mode_counts = ", ".join(f"{mode}:{count}" for mode, count in sorted(output_counts.items())) or output_mode
        duration = minutes_between(item.get("startedAt"), item.get("endedAt"))
        translations = int(item.get("translations") or 0)
        base_samples = safe_float(start_settings.get("baseGazeSamples"))
        dwell_seconds = round(base_samples / 300, 2) if base_samples else None
        item.update(
            {
                "username": str(item["username"]),
                "docName": item.get("docName") or "",
                "level": level_for_doc(item.get("docName") or ""),
                "durationMinutes": duration,
                "translationOutputMode": output_mode,
                "dominantTranslationOutputMode": dominant_output_mode,
                "firstTranslationOutputMode": first_output_mode,
                "finalTranslationOutputMode": final_output_mode,
                "translationOutputModeCounts": mode_counts,
                "translationOutputModeSwitches": mode_switch_count,
                "modeSelectionNote": "final_mode_used_after_mode_switch" if mode_switch_count else "single_mode",
                "trackerConnected": bool(item.get("trackerAddress") or item.get("trackerName")),
                "showGazeCursor": bool(start_settings.get("showGazeCursor")),
                "baseGazeSamples": base_samples,
                "dwellSeconds": dwell_seconds,
                "gazeHitRadiusPx": start_settings.get("gazeHitRadiusPx"),
                "translationsPerMinute": round(translations / duration, 2) if duration and duration > 0 else None,
                "maxTranslationGapSeconds": round(gaps.get(session_doc_key, 0.0), 2),
                "plausibleReadingSegment": bool(duration and duration >= 2.0),
            }
        )
        sessions.append(item)

    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for session in sessions:
        grouped[(str(session["username"]), str(session["docName"]))].append(session)
    return sessions, grouped


def load_all_session_summaries(conn: sqlite3.Connection) -> list[dict[str, object]]:
    rows = conn.execute(
        """
        SELECT s.sessionID, s.userID, u.username, s.startedAt, s.endedAt,
               s.endReason, s.startSettings,
               COUNT(e.eventID) AS events,
               GROUP_CONCAT(DISTINCT e.docName) AS docs,
               GROUP_CONCAT(DISTINCT COALESCE(e.translationOutputMode, 'on')) AS modes
        FROM user_sessions s
        JOIN users u ON u.userID = s.userID
        LEFT JOIN translation_events e ON e.sessionID = s.sessionID
        WHERE COALESCE(s.isHidden, 0) = 0
        GROUP BY s.sessionID
        ORDER BY u.username, s.startedAt
        """
    ).fetchall()
    summaries = []
    for row in rows:
        item = dict(row)
        item["username"] = str(item["username"])
        item["docs"] = item.get("docs") or "NO_TRANSLATION_EVENTS"
        item["modes"] = item.get("modes") or ""
        summaries.append(item)
    return summaries


def load_quiz_responses(
    username_to_id: dict[str, int], all_usernames: set[str], session_usernames: set[str]
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    quiz_responses = []
    question_stats_raw = []
    export_summaries = []

    for path in sorted(EXPORT_DIR.glob("*.zip")):
        lower_name = path.name.lower()
        if "sus" in lower_name or "experiment" in lower_name:
            continue
        member, rows, headers = read_zip_csv(path)
        doc_name = infer_doc_name(path, member)
        if not doc_name:
            export_summaries.append({"file": path.name, "type": "quiz", "rows": len(rows), "mapped_doc": "UNMAPPED"})
            continue
        id_col = id_column(headers)
        total_col = "Συνολική βαθμολογία" if "Συνολική βαθμολογία" in headers else None
        q_score_cols = score_columns(headers)
        export_summaries.append({"file": path.name, "type": "quiz", "rows": len(rows), "mapped_doc": doc_name})
        for row_idx, row in enumerate(rows, start=2):
            raw_id = clean_text(row.get(id_col, "") if id_col else "")
            username = normalize_user_id(raw_id, session_usernames, all_usernames)
            total, maximum = parse_score(row.get(total_col, "") if total_col else "")
            timestamp = parse_google_timestamp(row.get("Χρονική σήμανση", ""))
            score_pct = round(total / maximum * 100, 2) if total is not None and maximum else None
            response = {
                "sourceFile": path.name,
                "sourceMember": member,
                "rowNumber": row_idx,
                "timestamp": timestamp,
                "timestampRaw": row.get("Χρονική σήμανση", ""),
                "rawID": raw_id,
                "username": username,
                "docName": doc_name,
                "level": level_for_doc(doc_name),
                "score": total,
                "maxScore": maximum,
                "scorePercent": score_pct,
                "matchedKnownUser": username in username_to_id,
            }
            quiz_responses.append(response)

            for col in q_score_cols:
                q_score, q_max = parse_score(row.get(col, ""))
                if q_score is None or not q_max:
                    continue
                question = col.replace("[Βαθμολογία]", "").strip()
                question_stats_raw.append(
                    {
                        "sourceFile": path.name,
                        "rowNumber": row_idx,
                        "docName": doc_name,
                        "level": level_for_doc(doc_name),
                        "username": username,
                        "question": question,
                        "score": q_score,
                        "maxScore": q_max,
                        "correctPercent": q_score / q_max * 100 if q_max else None,
                    }
                )
    return quiz_responses, question_stats_raw, export_summaries


def session_match_sort_key(response: dict[str, object], session: dict[str, object]) -> tuple[object, ...]:
    submitted = response.get("timestamp")
    ended = parse_iso(session.get("endedAt"))
    started = parse_iso(session.get("startedAt"))
    duration = safe_float(session.get("durationMinutes")) or 0.0
    translations = int(session.get("translations") or 0)
    plausible = duration >= 2.0

    if isinstance(submitted, datetime) and ended:
        delay = (submitted - ended).total_seconds() / 60
        if delay >= -5:
            timing_rank = 0 if plausible else 1
        else:
            timing_rank = 2
        return (
            timing_rank,
            abs(delay),
            -duration,
            -translations,
            started if started else datetime.max,
        )

    return (
        0 if plausible else 1,
        -duration,
        -translations,
        started if started else datetime.max,
    )


def choose_session_for_response(response: dict[str, object], candidates: list[dict[str, object]]) -> dict[str, object]:
    return sorted(candidates, key=lambda session: session_match_sort_key(response, session))[0]


def join_quizzes_to_sessions(
    responses: list[dict[str, object]], sessions_by_key: dict[tuple[str, str], list[dict[str, object]]]
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    candidates_by_key: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    unmatched = []
    for response in responses:
        key = (str(response.get("username") or ""), str(response.get("docName") or ""))
        candidates = sessions_by_key.get(key, [])
        if not candidates:
            unmatched.append(response)
            continue
        session = choose_session_for_response(response, candidates)
        joined = {**response}
        joined["matchType"] = "db_session"
        joined["inferredConditionReason"] = ""
        joined.update({f"session_{k}": v for k, v in session.items()})
        joined["candidateSessionsForUserDoc"] = len(candidates)
        ended = parse_iso(session.get("endedAt"))
        submitted = response.get("timestamp")
        delay = None
        if ended and isinstance(submitted, datetime):
            delay = round((submitted - ended).total_seconds() / 60, 2)
        joined["quizDelayAfterSessionMinutes"] = delay
        candidates_by_key[key].append(joined)

    selected = []
    for key, candidates in candidates_by_key.items():
        def sort_key(row: dict[str, object]):
            delay = row.get("quizDelayAfterSessionMinutes")
            timestamp = row.get("timestamp")
            duration = safe_float(row.get("session_durationMinutes")) or 0.0
            translations = int(row.get("session_translations") or 0)
            # Prefer quiz responses submitted after the matched session. Then choose closest.
            if delay is None:
                return (2, 0 if duration >= 2.0 else 1, float("inf"), -duration, -translations, datetime.max)
            after_rank = 0 if delay >= -5 else 1
            plausible_rank = 0 if duration >= 2.0 else 1
            return (after_rank, plausible_rank, abs(delay), -duration, -translations, timestamp if isinstance(timestamp, datetime) else datetime.max)

        ordered = sorted(candidates, key=sort_key)
        chosen = ordered[0]
        chosen["duplicateQuizResponsesForUserDoc"] = len(candidates)
        selected.append(chosen)
    return selected, unmatched


def choose_quiz_response(candidates: list[dict[str, object]]) -> dict[str, object]:
    return sorted(candidates, key=lambda r: r.get("timestamp") if isinstance(r.get("timestamp"), datetime) else datetime.max)[0]


def infer_missing_condition_rows(
    quiz_responses: list[dict[str, object]],
    db_joined: list[dict[str, object]],
    unmatched: list[dict[str, object]],
    username_to_id: dict[str, int],
) -> list[dict[str, object]]:
    raw_by_user_doc: dict[str, dict[str, list[dict[str, object]]]] = defaultdict(lambda: defaultdict(list))
    for response in quiz_responses:
        username = str(response.get("username") or "")
        doc = str(response.get("docName") or "")
        if username in username_to_id and doc:
            raw_by_user_doc[username][doc].append(response)

    joined_by_user = defaultdict(list)
    for row in db_joined:
        joined_by_user[str(row.get("username") or "")].append(row)

    unmatched_keys = {(r.get("sourceFile"), r.get("rowNumber")) for r in unmatched}
    inferred = []
    for username, docs in raw_by_user_doc.items():
        if len(docs) != 8:
            continue
        user_joined = joined_by_user.get(username, [])
        joined_docs = {str(r.get("docName") or "") for r in user_joined}
        missing_docs = sorted(set(docs) - joined_docs)
        if not missing_docs:
            continue
        mode_counts = Counter(str(r.get("session_translationOutputMode") or "") for r in user_joined)
        on_deficit = 4 - mode_counts.get("on", 0)
        off_deficit = 4 - mode_counts.get("off", 0)
        if on_deficit < 0 or off_deficit < 0:
            continue
        if on_deficit + off_deficit != len(missing_docs):
            continue
        if on_deficit == len(missing_docs):
            inferred_mode = "on"
        elif off_deficit == len(missing_docs):
            inferred_mode = "off"
        else:
            # The total missing count is known, but the PDF-specific condition is ambiguous.
            continue

        for doc in missing_docs:
            candidates = [r for r in docs[doc] if (r.get("sourceFile"), r.get("rowNumber")) in unmatched_keys]
            if not candidates:
                continue
            response = choose_quiz_response(candidates)
            row = {**response}
            row.update(
                {
                    "matchType": "condition_inferred",
                    "inferredConditionReason": f"Ο user είχε 8 unique quiz PDFs και {mode_counts.get('on', 0)} popup-on / {mode_counts.get('off', 0)} popup-off DB-matched sessions. Για να συμπληρωθεί το αναμενόμενο 4-on/4-off, το missing PDF ταξινομήθηκε ως `{inferred_mode}`.",
                    "session_sessionID": "",
                    "session_startedAt": "",
                    "session_endedAt": "",
                    "session_endReason": "",
                    "session_durationMinutes": None,
                    "session_translationOutputMode": inferred_mode,
                    "session_firstTranslationOutputMode": "",
                    "session_dominantTranslationOutputMode": "",
                    "session_finalTranslationOutputMode": inferred_mode,
                    "session_translationOutputModeCounts": "",
                    "session_translationOutputModeSwitches": 0,
                    "session_modeSelectionNote": "condition_inferred_from_4_on_4_off_balance",
                    "session_trackerConnected": None,
                    "session_showGazeCursor": None,
                    "session_baseGazeSamples": None,
                    "session_dwellSeconds": None,
                    "session_translations": None,
                    "session_uniqueSourceWords": None,
                    "session_translationsPerMinute": None,
                    "session_maxTranslationGapSeconds": None,
                    "quizDelayAfterSessionMinutes": None,
                    "candidateSessionsForUserDoc": 0,
                    "duplicateQuizResponsesForUserDoc": len(candidates),
                }
            )
            inferred.append(row)
    return inferred


def unresolved_unmatched_rows(unmatched: list[dict[str, object]], inferred_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    inferred_keys = {(r.get("sourceFile"), r.get("rowNumber")) for r in inferred_rows}
    return [r for r in unmatched if (r.get("sourceFile"), r.get("rowNumber")) not in inferred_keys]


def add_pdf_normalized_scores(joined: list[dict[str, object]]) -> None:
    by_doc = defaultdict(list)
    for row in joined:
        if row.get("scorePercent") is not None:
            by_doc[row["docName"]].append(float(row["scorePercent"]))
    doc_stats = {doc: summarize(vals) for doc, vals in by_doc.items()}
    for row in joined:
        score = row.get("scorePercent")
        stats = doc_stats.get(row.get("docName"))
        if score is None or not stats or not stats.get("sd"):
            row["pdfNormalizedZ"] = None
        else:
            row["pdfNormalizedZ"] = round((float(score) - float(stats["mean"])) / float(stats["sd"]), 4)


def group_values(rows: list[dict[str, object]], key: str, metric: str) -> dict[str, list[float]]:
    groups = defaultdict(list)
    for row in rows:
        value = row.get(metric)
        if value is None:
            continue
        groups[str(row.get(key))].append(float(value))
    return groups


def table_group_summary(rows: list[dict[str, object]], key: str, metric: str = "scorePercent") -> list[dict[str, object]]:
    table = []
    for group, vals in group_values(rows, key, metric).items():
        stats = summarize(vals)
        table.append({"group": group, **stats})
    return sorted(table, key=lambda r: r["group"])


def interpret_pdf_condition_diff(diff: float | None, on_n: int, off_n: int) -> str:
    if diff is None:
        return "ανεπαρκή δεδομένα"
    if on_n < 8 or off_n < 8:
        confidence = "χαμηλή αξιοπιστία λόγω μικρού n"
    else:
        confidence = "usable n"
    if diff >= 10:
        direction = "ισχυρότερο score με popup-on"
    elif diff >= 5:
        direction = "πιθανό benefit με popup-on"
    elif diff <= -10:
        direction = "ισχυρότερο score με popup-off/external translation"
    elif diff <= -5:
        direction = "πιθανό benefit με popup-off/external translation"
    else:
        direction = "ουσιαστικά μικρή/ουδέτερη διαφορά"
    return f"{direction}; {confidence}"


def pdf_condition_comparison_rows(joined: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for doc in sorted({r["docName"] for r in joined}, key=lambda d: (LEVEL_ORDER.get(level_for_doc(d), 99), d)):
        on_vals = [float(r["scorePercent"]) for r in joined if r.get("docName") == doc and r.get("session_translationOutputMode") == "on" and r.get("scorePercent") is not None]
        off_vals = [float(r["scorePercent"]) for r in joined if r.get("docName") == doc and r.get("session_translationOutputMode") == "off" and r.get("scorePercent") is not None]
        on_stats = summarize(on_vals)
        off_stats = summarize(off_vals)
        diff = (mean(on_vals) or 0) - (mean(off_vals) or 0) if on_vals and off_vals else None
        rows.append(
            {
                "docName": doc,
                "level": level_for_doc(doc).upper(),
                "popup_on_n": on_stats["n"],
                "popup_on_mean": on_stats["mean"],
                "popup_on_median": on_stats["median"],
                "popup_on_sd": on_stats["sd"],
                "popup_off_n": off_stats["n"],
                "popup_off_mean": off_stats["mean"],
                "popup_off_median": off_stats["median"],
                "popup_off_sd": off_stats["sd"],
                "on_minus_off": diff,
                "cohens_d": pooled_d(on_vals, off_vals),
                "interpretation": interpret_pdf_condition_diff(diff, int(on_stats["n"] or 0), int(off_stats["n"] or 0)),
            }
        )
    return rows


def paired_condition_diffs(rows: list[dict[str, object]], condition_key: str, a_value: object, b_value: object, group_keys: list[str]) -> list[dict[str, object]]:
    grouped = defaultdict(lambda: defaultdict(list))
    for row in rows:
        score = row.get("scorePercent")
        if score is None:
            continue
        gkey = tuple(str(row.get(k)) for k in group_keys)
        grouped[gkey][str(row.get(condition_key))].append(float(score))
    diffs = []
    for gkey, values in grouped.items():
        avals = values.get(str(a_value), [])
        bvals = values.get(str(b_value), [])
        if avals and bvals:
            diffs.append({"group": gkey, "aMean": mean(avals), "bMean": mean(bvals), "diff": (mean(avals) or 0) - (mean(bvals) or 0)})
    return diffs


def chronological_value(row: dict[str, object]) -> datetime:
    started = parse_iso(row.get("session_startedAt"))
    if started:
        return started
    timestamp = row.get("timestamp")
    if isinstance(timestamp, datetime):
        return timestamp
    return datetime.max


def condition_balance_rows(joined: list[dict[str, object]]) -> list[dict[str, object]]:
    by_user = defaultdict(list)
    for row in joined:
        by_user[str(row.get("username") or "")].append(row)
    rows = []
    for username, items in sorted(by_user.items()):
        on = sum(1 for item in items if item.get("session_translationOutputMode") == "on")
        off = sum(1 for item in items if item.get("session_translationOutputMode") == "off")
        other = len(items) - on - off
        rows.append(
            {
                "username": username,
                "quiz_count": len(items),
                "popup_on": on,
                "popup_off": off,
                "other": other,
                "expected_8_total": len(items) == 8,
                "expected_4_on_4_off": len(items) == 8 and on == 4 and off == 4 and other == 0,
            }
        )
    return rows


def nearby_session_text(username: str, quiz_time: object, all_sessions: list[dict[str, object]]) -> str:
    if not isinstance(quiz_time, datetime):
        return "Δεν υπάρχει parsable quiz timestamp."
    lower = quiz_time - timedelta(minutes=45)
    upper = quiz_time + timedelta(minutes=15)
    same_user = [s for s in all_sessions if str(s.get("username") or "") == username]
    nearby = []
    for session in same_user:
        started = parse_iso(session.get("startedAt"))
        ended = parse_iso(session.get("endedAt")) or started
        if not started or not ended:
            continue
        if started <= upper and ended >= lower:
            nearby.append(session)
    if not nearby:
        same_day = []
        for session in same_user:
            started = parse_iso(session.get("startedAt"))
            if started and started.date() == quiz_time.date():
                same_day.append(session)
        if not same_day:
            return "Δεν βρέθηκε κοντινό session στο DB για την ίδια ημέρα."
        same_day = sorted(same_day, key=lambda s: abs(((parse_iso(s.get("startedAt")) or quiz_time) - quiz_time).total_seconds()))[:2]
        return "Δεν βρέθηκε session στο άμεσο χρονικό παράθυρο. Πιο κοντινά ίδιας ημέρας: " + "; ".join(format_session_evidence(s) for s in same_day)
    nearby = sorted(nearby, key=lambda s: parse_iso(s.get("startedAt")) or datetime.max)[:3]
    return "; ".join(format_session_evidence(s) for s in nearby)


def format_session_evidence(session: dict[str, object]) -> str:
    docs = clean_text(session.get("docs")) or "NO_TRANSLATION_EVENTS"
    modes = clean_text(session.get("modes")) or "-"
    events = session.get("events")
    return f"{session.get('startedAt')}->{session.get('endedAt')} docs={docs} modes={modes} events={events} reason={session.get('endReason')}"


def missing_session_review_rows(
    unresolved_unmatched: list[dict[str, object]],
    inferred_rows: list[dict[str, object]],
    all_sessions: list[dict[str, object]],
    username_to_id: dict[str, int],
) -> list[dict[str, object]]:
    rows = []
    for row in inferred_rows:
        rows.append(
            {
                "username": row.get("username"),
                "docName": row.get("docName"),
                "quizTimestamp": row.get("timestampRaw"),
                "status": "used_with_inferred_condition",
                "condition": row.get("session_translationOutputMode"),
                "reason": row.get("inferredConditionReason"),
                "nearbyEvidence": nearby_session_text(str(row.get("username") or ""), row.get("timestamp"), all_sessions),
            }
        )
    for row in unresolved_unmatched:
        username = str(row.get("username") or "")
        if username not in username_to_id:
            status = "unmatched_unknown_or_test_id"
            reason = "Το ID δεν αντιστοιχεί με γνωστό DB user, ή είναι κενό/test typo."
        else:
            status = "not_used_no_user_pdf_session"
            reason = "Υπάρχει quiz response, αλλά στο current DB δεν υπάρχει text session με ίδιο user και ίδιο PDF."
        rows.append(
            {
                "username": username,
                "docName": row.get("docName"),
                "quizTimestamp": row.get("timestampRaw"),
                "status": status,
                "condition": "",
                "reason": reason,
                "nearbyEvidence": nearby_session_text(username, row.get("timestamp"), all_sessions) if username else "",
            }
        )
    return sorted(rows, key=lambda r: (str(r.get("username")), str(r.get("quizTimestamp")), str(r.get("docName"))))


def progression_rows(joined: list[dict[str, object]]) -> list[dict[str, object]]:
    by_user = defaultdict(list)
    for row in joined:
        if row.get("scorePercent") is not None:
            by_user[str(row.get("username") or "")].append(row)

    rows = []
    for username, items in sorted(by_user.items()):
        ordered = sorted(items, key=chronological_value)
        if len(ordered) < 2:
            continue
        scores = [float(r["scorePercent"]) for r in ordered if r.get("scorePercent") is not None]
        zscores = [safe_float(r.get("pdfNormalizedZ")) for r in ordered]
        zscores_clean = [z for z in zscores if z is not None]
        first = ordered[0]
        last = ordered[-1]
        half = len(ordered) // 2
        first_half = ordered[:half]
        second_half = ordered[-half:] if half else []
        first_half_scores = [float(r["scorePercent"]) for r in first_half if r.get("scorePercent") is not None]
        second_half_scores = [float(r["scorePercent"]) for r in second_half if r.get("scorePercent") is not None]
        first_half_z = [safe_float(r.get("pdfNormalizedZ")) for r in first_half]
        second_half_z = [safe_float(r.get("pdfNormalizedZ")) for r in second_half]
        first_half_z = [z for z in first_half_z if z is not None]
        second_half_z = [z for z in second_half_z if z is not None]
        rows.append(
            {
                "username": username,
                "quiz_count": len(ordered),
                "first_doc": first.get("docName"),
                "last_doc": last.get("docName"),
                "first_mode": first.get("session_translationOutputMode"),
                "last_mode": last.get("session_translationOutputMode"),
                "first_score": float(first["scorePercent"]),
                "last_score": float(last["scorePercent"]),
                "first_last_change": float(last["scorePercent"]) - float(first["scorePercent"]),
                "first_z": safe_float(first.get("pdfNormalizedZ")),
                "last_z": safe_float(last.get("pdfNormalizedZ")),
                "first_last_z_change": (safe_float(last.get("pdfNormalizedZ")) or 0) - (safe_float(first.get("pdfNormalizedZ")) or 0)
                if safe_float(first.get("pdfNormalizedZ")) is not None and safe_float(last.get("pdfNormalizedZ")) is not None
                else None,
                "early_mean": mean(first_half_scores),
                "late_mean": mean(second_half_scores),
                "early_late_change": (mean(second_half_scores) or 0) - (mean(first_half_scores) or 0) if first_half_scores and second_half_scores else None,
                "early_z_mean": mean(first_half_z),
                "late_z_mean": mean(second_half_z),
                "early_late_z_change": (mean(second_half_z) or 0) - (mean(first_half_z) or 0) if first_half_z and second_half_z else None,
                "mean_score": mean(scores),
                "mean_z": mean(zscores_clean),
            }
        )
    return rows


def question_stats(question_rows: list[dict[str, object]], selected_joined: list[dict[str, object]]) -> list[dict[str, object]]:
    selected_keys = {(r["sourceFile"], r["rowNumber"]) for r in selected_joined}
    grouped = defaultdict(list)
    for row in question_rows:
        if (row["sourceFile"], row["rowNumber"]) not in selected_keys:
            continue
        if row.get("correctPercent") is None:
            continue
        grouped[(row["docName"], row["question"])].append(float(row["correctPercent"]))
    stats_rows = []
    for (doc, question), vals in grouped.items():
        s = summarize(vals)
        stats_rows.append({"docName": doc, "level": level_for_doc(doc), "question": question, **s})
    return sorted(stats_rows, key=lambda r: (r["mean"] if r["mean"] is not None else 999, r["docName"]))


def load_sus(username_to_id: dict[str, int], all_usernames: set[str], session_usernames: set[str]) -> tuple[list[dict[str, object]], list[dict[str, object]], list[str]]:
    paths = [p for p in EXPORT_DIR.glob("*.zip") if "sus" in p.name.lower()]
    if not paths:
        return [], [], []
    member, rows, headers = read_zip_csv(paths[0])
    user_col = "User ID"
    item_cols = [h for h in headers if h not in ("Χρονική σήμανση", user_col)]
    scored = []
    for idx, row in enumerate(rows, start=2):
        raw_id = row.get(user_col, "")
        username = normalize_user_id(raw_id, session_usernames, all_usernames)
        values = [parse_likert(row.get(col, "")) for col in item_cols]
        if any(v is None for v in values) or len(values) < 10:
            continue
        contributions = []
        for i, value in enumerate(values[:10], start=1):
            if i % 2 == 1:
                contributions.append(value - 1)
            else:
                contributions.append(5 - value)
        sus_score = sum(contributions) * 2.5
        scored.append(
            {
                "rowNumber": idx,
                "timestamp": parse_google_timestamp(row.get("Χρονική σήμανση", "")),
                "timestampRaw": row.get("Χρονική σήμανση", ""),
                "rawID": raw_id,
                "username": username,
                "matchedKnownUser": username in username_to_id,
                "susScore": sus_score,
                "rawValues": values[:10],
                "contributions": contributions,
            }
        )
    by_user = defaultdict(list)
    for row in scored:
        if row["username"] in username_to_id:
            by_user[row["username"]].append(row)
    paired = []
    for username, items in by_user.items():
        items = sorted(items, key=lambda r: r["timestamp"] or datetime.max)
        if len(items) < 2:
            continue
        first = items[0]
        last = items[-1]
        paired.append(
            {
                "username": username,
                "firstTimestamp": first["timestampRaw"],
                "secondTimestamp": last["timestampRaw"],
                "firstRawID": first["rawID"],
                "secondRawID": last["rawID"],
                "firstSUS": first["susScore"],
                "secondSUS": last["susScore"],
                "change": last["susScore"] - first["susScore"],
                "firstValues": first["rawValues"],
                "secondValues": last["rawValues"],
                "firstContrib": first["contributions"],
                "secondContrib": last["contributions"],
            }
        )
    return scored, paired, item_cols[:10]


def load_demographics(username_to_id: dict[str, int], all_usernames: set[str], session_usernames: set[str]) -> list[dict[str, object]]:
    paths = [p for p in EXPORT_DIR.glob("*.zip") if "experiment" in p.name.lower() and "sus" not in p.name.lower()]
    if not paths:
        return []
    _, rows, headers = read_zip_csv(paths[0])
    parsed = []
    for row in rows:
        raw_id = row.get("User ID", "")
        username = normalize_user_id(raw_id, session_usernames, all_usernames)
        parsed.append({**row, "username": username, "matchedKnownUser": username in username_to_id})
    return parsed


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    fieldnames = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            clean = {}
            for key, value in row.items():
                if isinstance(value, datetime):
                    clean[key] = value.isoformat(sep=" ")
                elif isinstance(value, (list, dict, tuple)):
                    clean[key] = json.dumps(value, ensure_ascii=False)
                else:
                    clean[key] = value
            writer.writerow(clean)


def md_table(headers: list[str], rows: list[list[object]]) -> list[str]:
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        out.append("| " + " | ".join(clean_text(c).replace("|", "/") for c in row) + " |")
    return out


def user_summary_rows(joined: list[dict[str, object]], sus_pairs: list[dict[str, object]]) -> list[dict[str, object]]:
    by_user = defaultdict(list)
    for row in joined:
        by_user[row["username"]].append(row)
    sus_by_user = {p["username"]: p for p in sus_pairs}
    rows = []
    for username, items in sorted(by_user.items()):
        scores = [float(r["scorePercent"]) for r in items if r.get("scorePercent") is not None]
        on = [float(r["scorePercent"]) for r in items if r.get("scorePercent") is not None and r.get("session_translationOutputMode") == "on"]
        off = [float(r["scorePercent"]) for r in items if r.get("scorePercent") is not None and r.get("session_translationOutputMode") == "off"]
        visible = [float(r["scorePercent"]) for r in items if r.get("scorePercent") is not None and r.get("session_showGazeCursor")]
        hidden = [float(r["scorePercent"]) for r in items if r.get("scorePercent") is not None and not r.get("session_showGazeCursor")]
        sus = sus_by_user.get(username)
        rows.append(
            {
                "username": username,
                "quiz_count": len(items),
                "mean_score_percent": round(mean(scores), 2) if scores else "",
                "popup_on_n": len(on),
                "popup_on_mean": round(mean(on), 2) if on else "",
                "popup_off_n": len(off),
                "popup_off_mean": round(mean(off), 2) if off else "",
                "popup_on_minus_off": round((mean(on) or 0) - (mean(off) or 0), 2) if on and off else "",
                "visible_cursor_n": len(visible),
                "visible_cursor_mean": round(mean(visible), 2) if visible else "",
                "hidden_cursor_n": len(hidden),
                "hidden_cursor_mean": round(mean(hidden), 2) if hidden else "",
                "sus_first": sus.get("firstSUS") if sus else "",
                "sus_second": sus.get("secondSUS") if sus else "",
                "sus_change": sus.get("change") if sus else "",
            }
        )
    return rows


def render_report(
    joined: list[dict[str, object]],
    unmatched: list[dict[str, object]],
    inferred_rows: list[dict[str, object]],
    missing_review: list[dict[str, object]],
    all_quiz_responses: list[dict[str, object]],
    export_summaries: list[dict[str, object]],
    sessions: list[dict[str, object]],
    sessions_by_key: dict[tuple[str, str], list[dict[str, object]]],
    qstats: list[dict[str, object]],
    sus_rows: list[dict[str, object]],
    sus_pairs: list[dict[str, object]],
    sus_item_cols: list[str],
    demographics: list[dict[str, object]],
) -> str:
    db_joined = [r for r in joined if r.get("matchType") == "db_session"]
    lines = []
    lines.append("# Quiz and Experiment Statistics Report")
    lines.append("")
    lines.append("Αυτό το report ενώνει τα Google Forms quiz exports με το current analysis database. Εστιάζει στο comprehension score, στο `translationOutputMode` (`on/off`), στη συμπεριφορά ανάγνωσης που έχει καταγραφεί στο DB, και στη μεταβολή του SUS μετά από χρήση του συστήματος.")
    lines.append("")
    lines.append("## Important Interpretation Notes")
    lines.append("")
    lines.append("- Σε αυτό το experiment το eye-tracker λειτουργεί και στις δύο συνθήκες.")
    lines.append("- Η βασική experimental condition είναι το `translationOutputMode`: `on` σημαίνει ότι ο participant έβλεπε το in-system translation popup κατά την ανάγνωση, ενώ `off` σημαίνει ότι δεν εμφανιζόταν popup και ο participant έπρεπε να χρησιμοποιήσει εξωτερικό εργαλείο/σελίδα μετάφρασης.")
    lines.append("- Όταν υπήρχαν πολλά sessions για το ίδιο user/PDF, το quiz response αντιστοιχίστηκε στο session που ταίριαζε καλύτερα χρονικά με το quiz, αποφεύγοντας πολύ σύντομα setup segments όταν υπήρχε πιο πιθανό reading session.")
    lines.append("- Αν ένα selected session άλλαξε popup mode μέσα στο ίδιο session, χρησιμοποιείται το final logged mode, επειδή αυτό πιθανότερα αντιστοιχεί στη διορθωμένη ρύθμιση μετά το αρχικό λάθος.")
    lines.append("- Αν υπάρχει quiz αλλά δεν βρέθηκε αντίστοιχο DB session, condition γίνεται inferred μόνο όταν ο user έχει ακριβώς 8 unique quiz PDFs και το missing mode προκύπτει μονοσήμαντα από το αναμενόμενο 4-on/4-off balance. Αυτά τα rows χρησιμοποιούνται μόνο για quiz/condition stats, όχι για behavioral correlations.")
    lines.append("- Το `showGazeCursor` αναφέρεται χωριστά. Είναι UI setting για το αν φαινόταν ο gaze cursor, όχι η βασική popup-translation condition.")
    lines.append("- Για να μειωθεί το bias από τη δυσκολία κάθε PDF, αναφέρονται και raw score percentages και PDF-normalized z-scores. Z-score πάνω από 0 σημαίνει ότι ο participant πήγε καλύτερα από τον μέσο όρο του ίδιου PDF quiz.")
    lines.append("- Τα αποτελέσματα είναι descriptive/observational summaries και όχι απόδειξη αιτιότητας. Το condition assignment, missing texts, timing corrections και duplicate setup sessions μπορούν να επηρεάσουν την ερμηνεία.")
    lines.append("")

    quiz_exports = [e for e in export_summaries if e["type"] == "quiz"]
    matched_scores = [float(r["scorePercent"]) for r in joined if r.get("scorePercent") is not None]
    lines.append("## Data Coverage")
    lines.append("")
    lines.extend(
        md_table(
            ["Metric", "Value"],
            [
                ["Quiz exports που διαβάστηκαν", len(quiz_exports)],
                ["Raw quiz responses", len(all_quiz_responses)],
                ["Πραγματικά DB-matched user/PDF quiz rows", len(db_joined)],
                ["Inferred condition-only quiz rows", len(inferred_rows)],
                ["Συνολικά quiz rows που χρησιμοποιούνται στα comprehension stats", len(joined)],
                ["Unresolved unmatched quiz responses", len(unmatched)],
                ["Candidate user/PDF pairs στο DB", len(sessions_by_key)],
                ["Unique DB sessions που χρησιμοποιήθηκαν μετά το matching", len({r.get("session_sessionID") for r in db_joined})],
                ["Participants με usable quiz data", len({r["username"] for r in joined})],
                ["Overall quiz score", fmt_summary_el(summarize(matched_scores))],
            ],
        )
    )
    lines.append("")
    if unmatched:
        unmatched_counts = Counter((r.get("rawID"), r.get("docName")) for r in unmatched)
        sample = list(unmatched_counts.items())[:15]
        lines.append("Τα unresolved unmatched responses είναι κυρίως blank/test IDs ή user/PDF quiz responses χωρίς αντίστοιχο DB session. Πρώτα παραδείγματα:")
        for (raw_id, doc), count in sample:
            lines.append(f"- `{raw_id}` / `{doc}`: {count} response(s)")
        lines.append("")

    balance = condition_balance_rows(joined)
    exact_total = sum(1 for row in balance if row["expected_8_total"])
    exact_condition = sum(1 for row in balance if row["expected_4_on_4_off"])
    balance_problems = [row for row in balance if not row["expected_4_on_4_off"]]
    mixed_mode_rows = [row for row in joined if int(row.get("session_translationOutputModeSwitches") or 0) > 0]
    multi_candidate_rows = [row for row in joined if int(row.get("candidateSessionsForUserDoc") or 1) > 1]
    lines.append("## Condition Assignment Check")
    lines.append("")
    lines.append("Το intended design είναι ένα quiz ανά text ανά participant, με 8 usable quiz/text observations ανά participant: 4 popup-on και 4 popup-off.")
    lines.extend(
        md_table(
            ["Metric", "Value"],
            [
                ["Participants με usable quiz data", len(balance)],
                ["Participants με ακριβώς 8 usable quizzes", exact_total],
                ["Participants με ακριβώς 4 popup-on και 4 popup-off", exact_condition],
                ["Participants που θέλουν condition/count review", len(balance_problems)],
                ["Rows που επιλέχθηκαν από user/PDFs με multiple candidate sessions", len(multi_candidate_rows)],
                ["Selected rows όπου το popup mode άλλαξε μέσα στο ίδιο session", len(mixed_mode_rows)],
            ],
        )
    )
    lines.append("")
    if balance_problems:
        lines.append("Participants που δεν ταιριάζουν στο expected 8 total / 4-on / 4-off pattern:")
        rows = []
        for row in balance_problems:
            rows.append([row["username"], row["quiz_count"], row["popup_on"], row["popup_off"], row["other"]])
        lines.extend(md_table(["User", "usable quizzes", "popup on", "popup off", "other"], rows))
        lines.append("")
    if mixed_mode_rows:
        lines.append("Selected session(s) με popup-mode switch μέσα στο ίδιο session. Για το condition label χρησιμοποιήθηκε το final mode:")
        rows = []
        for row in mixed_mode_rows:
            rows.append(
                [
                    row.get("username"),
                    row.get("docName"),
                    row.get("session_startedAt"),
                    row.get("session_endedAt"),
                    row.get("session_translationOutputModeCounts"),
                    row.get("session_translationOutputMode"),
                ]
            )
        lines.extend(md_table(["User", "PDF", "start", "end", "logged modes", "used mode"], rows))
        lines.append("")

    if missing_review:
        lines.append("### Missing Session Review")
        lines.append("")
        lines.append("Ο παρακάτω πίνακας εξηγεί γιατί κάποια quiz rows δεν έγιναν απλό DB match. Τα `used_with_inferred_condition` μπήκαν στα quiz/condition stats με inferred `on/off`. Τα `not_used_no_user_pdf_session` δεν μπήκαν στα stats γιατί δεν μπορούσε να βγει ασφαλές PDF-specific condition.")
        lines.append("Συμπέρασμα για τα ΑΜ με λιγότερα από 8 usable rows: στις περισσότερες περιπτώσεις το quiz υπάρχει στο Google Forms, αλλά στο current DB δεν υπάρχει `translation_events` row με το ίδιο user και το ίδιο PDF. Όταν το 4-on/4-off balance έκανε το missing condition μονοσήμαντο, το quiz κρατήθηκε ως inferred condition-only row.")
        review_rows = []
        for row in missing_review:
            if row.get("status") == "unmatched_unknown_or_test_id":
                continue
            review_rows.append([row.get("username"), row.get("docName"), row.get("quizTimestamp"), row.get("status"), row.get("condition"), shorten_text(row.get("reason"), 180), shorten_text(row.get("nearbyEvidence"), 220)])
        lines.extend(md_table(["User", "PDF", "quiz time", "status", "condition", "reason", "nearby DB evidence"], review_rows))
        lines.append("")

    lines.append("## Quiz Performance by Difficulty Level")
    level_rows = []
    for level in sorted({r["level"] for r in joined}, key=lambda x: LEVEL_ORDER.get(x, 99)):
        vals = [float(r["scorePercent"]) for r in joined if r["level"] == level and r.get("scorePercent") is not None]
        s = summarize(vals)
        level_rows.append([level.upper(), s["n"], fmt_num(s["mean"]), fmt_num(s["median"]), fmt_num(s["sd"]), f"{fmt_num(s['min'])}-{fmt_num(s['max'])}"])
    lines.extend(md_table(["Level", "n", "Μέσο %", "Διάμεσος %", "ΤΑ", "Εύρος"], level_rows))
    lines.append("")

    lines.append("## Quiz Performance by PDF")
    pdf_rows = []
    for doc in sorted({r["docName"] for r in joined}, key=lambda d: (LEVEL_ORDER.get(level_for_doc(d), 99), d)):
        vals = [float(r["scorePercent"]) for r in joined if r["docName"] == doc and r.get("scorePercent") is not None]
        s = summarize(vals)
        pdf_rows.append([doc, level_for_doc(doc).upper(), s["n"], fmt_num(s["mean"]), fmt_num(s["median"]), fmt_num(s["sd"])])
    lines.extend(md_table(["PDF", "Level", "n", "Μέσο %", "Διάμεσος %", "ΤΑ"], pdf_rows))
    lines.append("")

    pdf_condition_rows = pdf_condition_comparison_rows(joined)
    lines.append("## Popup On vs Off ανά PDF")
    lines.append("")
    lines.append("Εδώ συγκρίνεται κάθε κείμενο μόνο με τον εαυτό του: τι ποσοστό σωστών απαντήσεων είχαν οι participants όταν το ίδιο PDF διαβάστηκε με popup `on` σε σχέση με popup `off`. Αυτό είναι πιο καθαρό από το overall comparison, γιατί η δυσκολία του PDF μένει σταθερή μέσα σε κάθε row.")
    pdf_condition_table = []
    for row in pdf_condition_rows:
        pdf_condition_table.append(
            [
                row["docName"],
                row["level"],
                row["popup_on_n"],
                fmt_num(row["popup_on_mean"]),
                row["popup_off_n"],
                fmt_num(row["popup_off_mean"]),
                fmt_num(row["on_minus_off"]),
                fmt_num(row["cohens_d"], 3),
                row["interpretation"],
            ]
        )
    lines.extend(md_table(["PDF", "Level", "on n", "on μέσο %", "off n", "off μέσο %", "on-off", "d", "ερμηνεία"], pdf_condition_table))
    lines.append("")
    strongest_popup = [r for r in pdf_condition_rows if r.get("on_minus_off") is not None]
    strongest_popup = sorted(strongest_popup, key=lambda r: float(r["on_minus_off"]), reverse=True)
    if strongest_popup:
        best = strongest_popup[0]
        worst = strongest_popup[-1]
        neutral = [r for r in strongest_popup if abs(float(r["on_minus_off"])) < 5]
        popup_positive = [r for r in strongest_popup if float(r["on_minus_off"]) >= 5]
        popup_negative = [r for r in strongest_popup if float(r["on_minus_off"]) <= -5]
        lines.append(f"Σύντομη ανάγνωση: το μεγαλύτερο positive difference υπέρ του popup-on είναι στο `{best['docName']}` με {fmt_num(best['on_minus_off'])} percentage points. Το μεγαλύτερο negative difference είναι στο `{worst['docName']}` με {fmt_num(worst['on_minus_off'])} percentage points, δηλαδή καλύτερο score στο popup-off/external translation.")
        lines.append(f"Με threshold ±5 percentage points: {len(popup_positive)} PDFs δείχνουν πιθανό benefit υπέρ popup-on, {len(popup_negative)} PDFs δείχνουν πιθανό benefit υπέρ popup-off/external translation, και {len(neutral)} PDFs είναι πρακτικά ουδέτερα.")
        lines.append("")

    lines.append("## Popup Translation Output: On vs Off")
    lines.append("")
    lines.append("Αυτή είναι η βασική experimental comparison. Και στις δύο περιπτώσεις το eye-tracker ήταν ενεργό. `on` σημαίνει ότι ο participant έβλεπε το translation popup μέσα στο reading system. `off` σημαίνει ότι έπρεπε να μεταφράσει εξωτερικά, π.χ. με Google Translate.")
    popup_rows = []
    for mode in ("on", "off"):
        vals = [float(r["scorePercent"]) for r in joined if r.get("session_translationOutputMode") == mode and r.get("scorePercent") is not None]
        zvals = [float(r["pdfNormalizedZ"]) for r in joined if r.get("session_translationOutputMode") == mode and r.get("pdfNormalizedZ") is not None]
        s = summarize(vals)
        zs = summarize(zvals)
        popup_rows.append([mode, s["n"], fmt_num(s["mean"]), fmt_num(s["median"]), fmt_num(s["sd"]), fmt_num(zs["mean"], 3), fmt_num(zs["median"], 3)])
    lines.extend(md_table(["Popup mode", "n", "Μέσο %", "Διάμεσος %", "ΤΑ", "Μέσο PDF-z", "Διάμεσος PDF-z"], popup_rows))
    lines.append("")
    on_vals = [float(r["scorePercent"]) for r in joined if r.get("session_translationOutputMode") == "on" and r.get("scorePercent") is not None]
    off_vals = [float(r["scorePercent"]) for r in joined if r.get("session_translationOutputMode") == "off" and r.get("scorePercent") is not None]
    lines.append(f"Raw popup-on μείον popup-off μέση διαφορά: **{fmt_num((mean(on_vals) or 0) - (mean(off_vals) or 0))} percentage points**; independent-groups Cohen's d = **{fmt_num(pooled_d(on_vals, off_vals), 3)}**.")
    z_on = [float(r["pdfNormalizedZ"]) for r in joined if r.get("session_translationOutputMode") == "on" and r.get("pdfNormalizedZ") is not None]
    z_off = [float(r["pdfNormalizedZ"]) for r in joined if r.get("session_translationOutputMode") == "off" and r.get("pdfNormalizedZ") is not None]
    lines.append(f"PDF-normalized popup-on μείον popup-off μέση διαφορά: **{fmt_num((mean(z_on) or 0) - (mean(z_off) or 0), 3)} z-score units**.")
    lines.append("")

    popup_level_rows = []
    for level in sorted({r["level"] for r in joined}, key=lambda x: LEVEL_ORDER.get(x, 99)):
        for mode in ("on", "off"):
            vals = [float(r["scorePercent"]) for r in joined if r["level"] == level and r.get("session_translationOutputMode") == mode and r.get("scorePercent") is not None]
            s = summarize(vals)
            popup_level_rows.append([level.upper(), mode, s["n"], fmt_num(s["mean"]), fmt_num(s["median"]), fmt_num(s["sd"])])
    lines.append("### Popup Mode by Level")
    lines.extend(md_table(["Level", "Popup", "n", "Μέσο %", "Διάμεσος %", "ΤΑ"], popup_level_rows))
    lines.append("")

    user_popup_diffs = paired_condition_diffs(joined, "session_translationOutputMode", "on", "off", ["username"])
    diffs = [float(d["diff"]) for d in user_popup_diffs]
    lines.append("### Within-Participant Popup Comparison")
    lines.append(f"Participants με popup-on και popup-off quiz rows: **{len(diffs)}**.")
    if diffs:
        lines.append(f"Μέση within-participant διαφορά popup-on μείον popup-off: **{fmt_num(mean(diffs))} percentage points**; διάμεσος **{fmt_num(median(diffs))}**; paired Cohen's d = **{fmt_num(paired_d(diffs), 3)}**.")
        lines.append(f"Users με υψηλότερο score στο popup-on / ίσο / υψηλότερο στο popup-off: **{sum(1 for d in diffs if d > 0)} / {sum(1 for d in diffs if d == 0)} / {sum(1 for d in diffs if d < 0)}**.")
    level_pair_rows = []
    for level in sorted({r["level"] for r in joined}, key=lambda x: LEVEL_ORDER.get(x, 99)):
        level_diffs = [float(d["diff"]) for d in paired_condition_diffs([r for r in joined if r["level"] == level], "session_translationOutputMode", "on", "off", ["username"])]
        if level_diffs:
            s = summarize(level_diffs)
            level_pair_rows.append([level.upper(), s["n"], fmt_num(s["mean"]), fmt_num(s["median"]), fmt_num(s["sd"]), fmt_num(paired_d(level_diffs), 3)])
    if level_pair_rows:
        lines.extend(md_table(["Level", "paired users", "Μέσο on-off", "Διάμεσος", "ΤΑ", "paired d"], level_pair_rows))
    lines.append("")

    if diffs:
        diff_rows = []
        for item in sorted(user_popup_diffs, key=lambda d: abs(float(d["diff"])), reverse=True)[:15]:
            diff_rows.append([item["group"][0], fmt_num(item["aMean"]), fmt_num(item["bMean"]), fmt_num(item["diff"])])
        lines.append("### Largest Individual Popup Differences")
        lines.append("Θετικές τιμές σημαίνουν ότι ο participant είχε υψηλότερο score με το in-system popup. Αρνητικές τιμές σημαίνουν υψηλότερο score όταν χρησιμοποιούσε εξωτερική μετάφραση.")
        lines.extend(md_table(["User", "popup-on μέσο %", "popup-off μέσο %", "on-off"], diff_rows))
        lines.append("")

    lines.append("## Eye-Tracker and Gaze-Cursor Fields")
    lines.append("")
    tracker_connected = Counter(bool(r.get("session_trackerConnected")) for r in db_joined)
    lines.append(f"Όλα τα πραγματικά DB-matched quiz/session rows έχουν tracker connection: **{tracker_connected.get(True, 0)} / {len(db_joined)}**. Rows χωρίς tracker connection: **{tracker_connected.get(False, 0)}**.")
    lines.append("Αυτό επιβεβαιώνει ότι οι συνθήκες popup-on και popup-off είναι και οι δύο eye-tracker sessions. Τα inferred condition-only rows δεν μετριούνται εδώ, επειδή δεν έχουν πραγματικό DB session row.")
    lines.append("")
    cursor_rows = []
    for visible in (True, False):
        vals = [float(r["scorePercent"]) for r in db_joined if bool(r.get("session_showGazeCursor")) == visible and r.get("scorePercent") is not None]
        zvals = [float(r["pdfNormalizedZ"]) for r in db_joined if bool(r.get("session_showGazeCursor")) == visible and r.get("pdfNormalizedZ") is not None]
        s = summarize(vals)
        zs = summarize(zvals)
        cursor_rows.append(["visible" if visible else "hidden", s["n"], fmt_num(s["mean"]), fmt_num(s["median"]), fmt_num(s["sd"]), fmt_num(zs["mean"], 3)])
    lines.append("### Gaze Cursor Visible vs Hidden")
    lines.extend(md_table(["Gaze cursor", "n", "Μέσο %", "Διάμεσος %", "ΤΑ", "Μέσο PDF-z"], cursor_rows))
    lines.append("")
    visible_vals = [float(r["scorePercent"]) for r in db_joined if bool(r.get("session_showGazeCursor")) and r.get("scorePercent") is not None]
    hidden_vals = [float(r["scorePercent"]) for r in db_joined if not bool(r.get("session_showGazeCursor")) and r.get("scorePercent") is not None]
    lines.append(f"Raw visible-minus-hidden μέση διαφορά: **{fmt_num((mean(visible_vals) or 0) - (mean(hidden_vals) or 0))} percentage points**. Αυτό πρέπει να ερμηνευτεί μόνο ως UI/gaze-cursor comparison. Η βασική experimental condition παραμένει το popup translation on/off.")
    lines.append("")

    dwell_rows = []
    for dwell in sorted({r.get("session_dwellSeconds") for r in db_joined if r.get("session_dwellSeconds") is not None}):
        vals = [float(r["scorePercent"]) for r in db_joined if r.get("session_dwellSeconds") == dwell and r.get("scorePercent") is not None]
        if len(vals) < 5:
            continue
        s = summarize(vals)
        dwell_rows.append([fmt_num(dwell), s["n"], fmt_num(s["mean"]), fmt_num(s["median"]), fmt_num(s["sd"])])
    if dwell_rows:
        lines.append("### Gaze Dwell Time Before Translation")
        lines.append("Το `baseGazeSamples / 300` δίνει περίπου τον χρόνο gaze dwell σε δευτερόλεπτα πριν επιλεγεί μια λέξη για μετάφραση.")
        lines.extend(md_table(["Dwell sec", "n", "Μέσο %", "Διάμεσος %", "ΤΑ"], dwell_rows))
        lines.append("")

    lines.append("## Behavioural Correlations")
    lines.append("")
    variables = [
        ("Διάρκεια ανάγνωσης σε λεπτά", "session_durationMinutes"),
        ("Πλήθος μεταφράσεων", "session_translations"),
        ("Unique translated source words", "session_uniqueSourceWords"),
        ("Μεταφράσεις ανά λεπτό", "session_translationsPerMinute"),
        ("Μέγιστο κενό ανάμεσα σε μεταφράσεις, sec", "session_maxTranslationGapSeconds"),
        ("Quiz delay μετά το session, λεπτά", "quizDelayAfterSessionMinutes"),
        ("Gaze dwell seconds", "session_dwellSeconds"),
    ]
    corr_rows = []
    y = [float(r["scorePercent"]) for r in joined if r.get("scorePercent") is not None]
    for label, key in variables:
        pairs = [(safe_float(r.get(key)), safe_float(r.get("scorePercent"))) for r in joined]
        xs = [p[0] for p in pairs if p[0] is not None and p[1] is not None]
        ys = [p[1] for p in pairs if p[0] is not None and p[1] is not None]
        corr_rows.append([label, len(xs), fmt_num(pearson(xs, ys), 3), fmt_num(spearman(xs, ys), 3)])
    lines.extend(md_table(["Variable", "n", "Pearson r με score", "Spearman rho"], corr_rows))
    lines.append("")

    progress = progression_rows(joined)
    if progress:
        first_last = [float(r["first_last_change"]) for r in progress if r.get("first_last_change") is not None]
        first_last_z = [float(r["first_last_z_change"]) for r in progress if r.get("first_last_z_change") is not None]
        early_late = [float(r["early_late_change"]) for r in progress if r.get("early_late_change") is not None]
        early_late_z = [float(r["early_late_z_change"]) for r in progress if r.get("early_late_z_change") is not None]
        complete_progress = [r for r in progress if int(r.get("quiz_count") or 0) == 8]
        complete_early_late_z = [float(r["early_late_z_change"]) for r in complete_progress if r.get("early_late_z_change") is not None]
        lines.append("## Change Over Time")
        lines.append("")
        lines.append("Τα rows μπήκαν σε χρονολογική σειρά με βάση το matched DB session start time. Για inferred condition-only rows, όπου δεν υπάρχει DB session time, χρησιμοποιείται το quiz timestamp. Το raw score change είναι χρήσιμο, αλλά το PDF-normalized z-score change είναι ασφαλέστερο επειδή το πρώτο και τελευταίο text μπορεί να μην έχουν ίδια δυσκολία.")
        lines.extend(
            md_table(
                ["Metric", "Value"],
                [
                    ["Users με τουλάχιστον 2 usable quiz rows", len(progress)],
                    ["First quiz to last quiz raw change", fmt_summary_el(summarize(first_last))],
                    ["First quiz to last quiz PDF-z change", fmt_summary_el(summarize(first_last_z))],
                    ["Early half to late half raw change", fmt_summary_el(summarize(early_late))],
                    ["Early half to late half PDF-z change", fmt_summary_el(summarize(early_late_z))],
                    ["Complete 8-quiz users: early half to late half PDF-z change", fmt_summary_el(summarize(complete_early_late_z))],
                    ["PDF-z improved / unchanged / declined, all users", f"{sum(1 for v in early_late_z if v > 0)} / {sum(1 for v in early_late_z if v == 0)} / {sum(1 for v in early_late_z if v < 0)}"],
                    ["PDF-z improved / unchanged / declined, complete users", f"{sum(1 for v in complete_early_late_z if v > 0)} / {sum(1 for v in complete_early_late_z if v == 0)} / {sum(1 for v in complete_early_late_z if v < 0)}"],
                ],
            )
        )
        lines.append("")
        strongest_progress = sorted(progress, key=lambda r: abs(float(r.get("early_late_z_change") or 0)), reverse=True)[:12]
        lines.append("Οι μεγαλύτερες individual early-to-late μεταβολές μετά από PDF normalization:")
        rows = []
        for row in strongest_progress:
            rows.append([row["username"], row["quiz_count"], fmt_num(row["early_z_mean"], 3), fmt_num(row["late_z_mean"], 3), fmt_num(row["early_late_z_change"], 3), row["first_doc"], row["last_doc"]])
        lines.extend(md_table(["User", "quizzes", "early z", "late z", "late-early z", "first PDF", "last PDF"], rows))
        lines.append("")

    lines.append("## Hardest Quiz Questions")
    lines.append("")
    lines.append("Οι ερωτήσεις με τα χαμηλότερα average question scores στα usable responses. Αυτό βοηθά να εντοπιστούν comprehension items που ήταν γενικά δύσκολα, ανεξάρτητα από το system condition.")
    hard_rows = []
    for row in qstats[:15]:
        hard_rows.append([row["docName"], row["level"].upper(), row["n"], fmt_num(row["mean"]), clean_text(row["question"])[:120]])
    lines.extend(md_table(["PDF", "Level", "n", "Μέσο question %", "Question"], hard_rows))
    lines.append("")

    lines.append("## SUS Usability Change")
    lines.append("")
    lines.append("Το SUS υπολογίστηκε με την standard 0-100 formula: τα odd items δίνουν `response - 1`, τα even items δίνουν `5 - response`, και το άθροισμα πολλαπλασιάζεται με 2.5. Υψηλότερο score σημαίνει καλύτερη perceived usability.")
    sus_valid = [r for r in sus_rows if r.get("matchedKnownUser")]
    first_scores = [float(p["firstSUS"]) for p in sus_pairs]
    second_scores = [float(p["secondSUS"]) for p in sus_pairs]
    changes = [float(p["change"]) for p in sus_pairs]
    lines.extend(
        md_table(
            ["Metric", "Value"],
            [
                ["Valid matched SUS submissions", len(sus_valid)],
                ["Participants με paired first/last SUS", len(sus_pairs)],
                ["First SUS", fmt_summary_el(summarize(first_scores))],
                ["Second SUS", fmt_summary_el(summarize(second_scores))],
                ["Change second-first", fmt_summary_el(summarize(changes))],
                ["Paired Cohen's d for SUS change", fmt_num(paired_d(changes), 3)],
                ["Improved / unchanged / declined", f"{sum(1 for c in changes if c > 0)} / {sum(1 for c in changes if c == 0)} / {sum(1 for c in changes if c < 0)}"],
                ["First SUS >= 68", f"{sum(1 for s in first_scores if s >= 68)} / {len(first_scores)}"],
                ["Second SUS >= 68", f"{sum(1 for s in second_scores if s >= 68)} / {len(second_scores)}"],
            ],
        )
    )
    lines.append("")
    if sus_pairs and sus_item_cols:
        item_rows = []
        for idx, col in enumerate(sus_item_cols):
            first = [p["firstContrib"][idx] for p in sus_pairs]
            second = [p["secondContrib"][idx] for p in sus_pairs]
            diffs = [b - a for a, b in zip(first, second)]
            item_rows.append([idx + 1, fmt_num(mean(first)), fmt_num(mean(second)), fmt_num(mean(diffs)), clean_text(col)[:100]])
        lines.append("### SUS Item-Level Change")
        lines.append("Τα item scores παρακάτω είναι ήδη direction-corrected, άρα υψηλότερο σημαίνει πάντα καλύτερη αξιολόγηση.")
        lines.extend(md_table(["Item", "First mean", "Second mean", "Mean change", "Statement"], item_rows))
        lines.append("")

    lines.append("## Participant Background")
    lines.append("")
    matched_demo = [d for d in demographics if d.get("matchedKnownUser")]
    ages = [safe_float(d.get("Ηλικία")) for d in matched_demo]
    ages = [a for a in ages if a is not None]
    lines.extend(
        md_table(
            ["Metric", "Value"],
            [
                ["Demographic rows", len(demographics)],
                ["Matched demographic rows", len(matched_demo)],
                ["Age", fmt_summary_el(summarize(ages))],
            ],
        )
    )
    lines.append("")
    for col, label in [
        ("Φύλο", "Gender"),
        ("Πώς θα αξιολογούσατε το επίπεδο αγγλικών σας;", "Self-rated English level"),
        ("Πόσο συχνά χρησιμοποιείτε εργαλεία μετάφρασης;\n", "Translation tool use frequency"),
        ("Αντιμετωπίζετε κάποια μαθησιακή δυσκολία ή δυσκολία ανάγνωσης που θα θέλατε να αναφέρετε;", "Reported reading/learning difficulty"),
    ]:
        counts = Counter(clean_text(d.get(col)) or "blank" for d in matched_demo)
        if counts:
            lines.append(f"### {label}")
            lines.extend(md_table(["Response", "n"], [[k, v] for k, v in counts.most_common()]))
            lines.append("")

    # Demographics and score, especially English level.
    score_by_user = defaultdict(list)
    for row in joined:
        if row.get("scorePercent") is not None:
            score_by_user[row["username"]].append(float(row["scorePercent"]))
    demo_by_user = {d.get("username"): d for d in matched_demo}
    english_groups = defaultdict(list)
    for username, scores in score_by_user.items():
        demo = demo_by_user.get(username)
        if not demo:
            continue
        level = clean_text(demo.get("Πώς θα αξιολογούσατε το επίπεδο αγγλικών σας;")) or "blank"
        english_groups[level].append(mean(scores) or 0)
    if english_groups:
        lines.append("### Quiz Score by Self-Rated English Level")
        rows = []
        for level, vals in sorted(english_groups.items()):
            s = summarize(vals)
            rows.append([level, s["n"], fmt_num(s["mean"]), fmt_num(s["median"]), fmt_num(s["sd"])])
        lines.extend(md_table(["English level", "participants", "Μέσο user quiz %", "Διάμεσος", "ΤΑ"], rows))
        lines.append("")

    lines.append("## Per-Participant Summary")
    lines.append("")
    lines.append(f"Το πλήρες per-participant table γράφτηκε στο `{USER_SUMMARY_CSV.name}`. Παρακάτω φαίνονται τα πρώτα rows.")
    user_rows = user_summary_rows(joined, sus_pairs)
    preview = []
    for row in user_rows[:25]:
        preview.append([row["username"], row["quiz_count"], row["mean_score_percent"], row["popup_on_mean"], row["popup_off_mean"], row["popup_on_minus_off"], row["sus_change"]])
    lines.extend(md_table(["User", "quizzes", "Μέσο %", "Popup on %", "Popup off %", "On-off", "SUS change"], preview))
    lines.append("")

    lines.append("## Main Conclusions and Hypotheses")
    lines.append("")
    popup_raw_diff = (mean(on_vals) or 0) - (mean(off_vals) or 0)
    popup_z_diff = (mean(z_on) or 0) - (mean(z_off) or 0)
    popup_diffs_for_conclusion = [float(d["diff"]) for d in user_popup_diffs]
    level_means = []
    for level in sorted({r["level"] for r in joined}, key=lambda x: LEVEL_ORDER.get(x, 99)):
        vals = [float(r["scorePercent"]) for r in joined if r["level"] == level and r.get("scorePercent") is not None]
        level_means.append((level.upper(), mean(vals) or 0))
    hardest_doc = None
    easiest_doc = None
    doc_mean_rows = []
    for doc in sorted({r["docName"] for r in joined}):
        vals = [float(r["scorePercent"]) for r in joined if r["docName"] == doc and r.get("scorePercent") is not None]
        if vals:
            doc_mean_rows.append((doc, mean(vals) or 0))
    if doc_mean_rows:
        hardest_doc = min(doc_mean_rows, key=lambda item: item[1])
        easiest_doc = max(doc_mean_rows, key=lambda item: item[1])
    progress_again = progression_rows(joined)
    late_z_changes = [float(r["early_late_z_change"]) for r in progress_again if r.get("early_late_z_change") is not None]
    sus_change_mean = mean([float(p["change"]) for p in sus_pairs]) if sus_pairs else None
    lines.append(f"- Η popup condition **δεν έδειξε ουσιαστικό overall comprehension-score advantage**. Η raw διαφορά popup-on μείον popup-off ήταν {fmt_num(popup_raw_diff)} percentage points, και η PDF-normalized διαφορά ήταν {fmt_num(popup_z_diff, 3)} z-score units.")
    if popup_diffs_for_conclusion:
        lines.append(f"- Τα individual responses ήταν ετερογενή: {sum(1 for d in popup_diffs_for_conclusion if d > 0)} users είχαν καλύτερο μέσο score με popup, {sum(1 for d in popup_diffs_for_conclusion if d < 0)} είχαν καλύτερο μέσο score με external translation, και {sum(1 for d in popup_diffs_for_conclusion if d == 0)} ήταν ίσοι με βάση τα condition means.")
    if hardest_doc and easiest_doc:
        lines.append(f"- Η δυσκολία του text φαίνεται να είχε μεγαλύτερη επίδραση από το popup mode. Το χαμηλότερο-scoring PDF ήταν το `{hardest_doc[0]}` με {fmt_num(hardest_doc[1])}%, ενώ το υψηλότερο-scoring PDF ήταν το `{easiest_doc[0]}` με {fmt_num(easiest_doc[1])}%.")
    if level_means:
        level_text = ", ".join(f"{level}: {fmt_num(value)}%" for level, value in level_means)
        lines.append(f"- Ανά level, οι observed means ήταν {level_text}. Το C2 average πέφτει αρκετά λόγω του `c2_rosa_parks_2.pdf`, άρα τα level effects πρέπει να συζητηθούν μαζί με individual text effects.")
    pdf_condition_for_conclusion = [r for r in pdf_condition_rows if r.get("on_minus_off") is not None]
    if pdf_condition_for_conclusion:
        pdf_popup_positive = [r for r in pdf_condition_for_conclusion if float(r["on_minus_off"]) >= 5]
        pdf_popup_negative = [r for r in pdf_condition_for_conclusion if float(r["on_minus_off"]) <= -5]
        pdf_neutral = [r for r in pdf_condition_for_conclusion if abs(float(r["on_minus_off"])) < 5]
        lines.append(f"- Στο per-PDF comparison η εικόνα είναι μικτή: {len(pdf_popup_positive)} PDFs έχουν διαφορά τουλάχιστον +5 points υπέρ popup-on, {len(pdf_popup_negative)} PDFs έχουν διαφορά τουλάχιστον -5 points υπέρ popup-off/external translation, και {len(pdf_neutral)} PDFs είναι εντός ±5 points.")
    if late_z_changes:
        lines.append(f"- Δεν υπάρχει ισχυρή ένδειξη για μεγάλο learning/practice improvement στα quiz scores με την πάροδο του χρόνου. Η early-to-late PDF-normalized μεταβολή είχε μέσο {fmt_num(mean(late_z_changes), 3)} z-score units, με {sum(1 for v in late_z_changes if v > 0)} users να βελτιώνονται και {sum(1 for v in late_z_changes if v < 0)} να μειώνονται.")
    lines.append("- Τα behavioural correlations με το score ήταν weak. Το translation count και τα translations per minute ήταν ελαφρώς αρνητικά, κάτι που πιθανότερα σημαίνει ότι readers με χαμηλότερη κατανόηση χρειάζονταν περισσότερη μεταφραστική υποστήριξη, όχι ότι η μετάφραση προκάλεσε χαμηλότερο score.")
    if sus_change_mean is not None:
        lines.append(f"- Το SUS usability ήταν ήδη υψηλό και αυξήθηκε ελαφρά με τη χρήση. Το mean SUS change ήταν {fmt_num(sus_change_mean)} points, κάτι που δείχνει ότι το σύστημα παρέμεινε αποδεκτό μετά από επαναλαμβανόμενη χρήση αντί να γίνεται πιο κουραστικό/frustrating.")
    lines.append("- Για πιο ισχυρά statistical claims θα χρειαζόταν mixed-effects model με participant και PDF ως random effects. Τα descriptive statistics εδώ παραμένουν χρήσιμα γιατί δείχνουν το βασικό pattern: οι διαφορές στο score φαίνεται να οδηγούνται περισσότερο από participant/text variation παρά από το popup-on versus popup-off μόνο.")
    lines.append("")

    lines.append("## Data Quality Notes")
    lines.append("")
    duplicate_count = sum(1 for r in joined if int(r.get("duplicateQuizResponsesForUserDoc") or 1) > 1)
    lines.append(f"- User/PDF pairs με duplicate quiz responses όπου επιλέχθηκε ένα response με βάση timestamp proximity: **{duplicate_count}**.")
    lines.append(f"- Τα matched quiz rows με accepted/split timing corrections χρησιμοποιούν τις current analysis DB values. Αν κάποιο session end time είναι ακόμη λάθος, τα duration-based correlations μπορούν να αλλάξουν.")
    lines.append(f"- Τα popup condition labels προέρχονται από το `translationOutputMode`. Για sessions με multiple candidate DB segments, το matching χρησιμοποιεί το quiz timestamp και αποφεύγει short setup segments όπου είναι δυνατό.")
    lines.append(f"- Τα inferred condition-only rows δεν δημιουργούν νέο session και δεν αλλάζουν το DB. Απλώς κρατούν το quiz score στο condition analysis όταν το 4-on/4-off balance κάνει το missing condition μονοσήμαντο.")
    lines.append("")
    lines.append("## Output Files")
    lines.append("")
    lines.append(f"- Joined quiz/session data: `{JOINED_CSV.name}`")
    lines.append(f"- Per-participant summary: `{USER_SUMMARY_CSV.name}`")
    lines.append(f"- SUS paired data: `{SUS_PAIRED_CSV.name}`")
    lines.append(f"- Question-level statistics: `{QUESTION_STATS_CSV.name}`")
    lines.append(f"- Missing-session review: `{MISSING_SESSION_REVIEW_CSV.name}`")
    lines.append(f"- PDF condition comparison: `{PDF_CONDITION_COMPARISON_CSV.name}`")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    ensure_analysis_schema(conn)
    username_to_id, all_usernames, session_usernames = get_db_users(conn)
    sessions, sessions_by_key = load_sessions(conn)
    all_session_summaries = load_all_session_summaries(conn)
    quiz_responses, qrows, export_summaries = load_quiz_responses(username_to_id, all_usernames, session_usernames)
    db_joined, unmatched_raw = join_quizzes_to_sessions(quiz_responses, sessions_by_key)
    inferred_rows = infer_missing_condition_rows(quiz_responses, db_joined, unmatched_raw, username_to_id)
    unmatched = unresolved_unmatched_rows(unmatched_raw, inferred_rows)
    joined = db_joined + inferred_rows
    add_pdf_normalized_scores(joined)
    qstats = question_stats(qrows, joined)
    sus_rows, sus_pairs, sus_item_cols = load_sus(username_to_id, all_usernames, session_usernames)
    demographics = load_demographics(username_to_id, all_usernames, session_usernames)
    missing_review = missing_session_review_rows(unmatched, inferred_rows, all_session_summaries, username_to_id)

    # CSV outputs
    joined_csv_rows = []
    for row in sorted(joined, key=lambda r: (str(r.get("username")), str(r.get("docName")))):
        joined_csv_rows.append(
            {
                "username": row.get("username"),
                "docName": row.get("docName"),
                "matchType": row.get("matchType"),
                "inferredConditionReason": row.get("inferredConditionReason"),
                "level": row.get("level"),
                "score": row.get("score"),
                "maxScore": row.get("maxScore"),
                "scorePercent": row.get("scorePercent"),
                "pdfNormalizedZ": row.get("pdfNormalizedZ"),
                "quizTimestamp": row.get("timestamp"),
                "sessionID": row.get("session_sessionID"),
                "startedAt": row.get("session_startedAt"),
                "endedAt": row.get("session_endedAt"),
                "endReason": row.get("session_endReason"),
                "durationMinutes": row.get("session_durationMinutes"),
                "translationOutputMode": row.get("session_translationOutputMode"),
                "firstTranslationOutputMode": row.get("session_firstTranslationOutputMode"),
                "dominantTranslationOutputMode": row.get("session_dominantTranslationOutputMode"),
                "finalTranslationOutputMode": row.get("session_finalTranslationOutputMode"),
                "translationOutputModeCounts": row.get("session_translationOutputModeCounts"),
                "translationOutputModeSwitches": row.get("session_translationOutputModeSwitches"),
                "modeSelectionNote": row.get("session_modeSelectionNote"),
                "trackerConnected": row.get("session_trackerConnected"),
                "showGazeCursor": row.get("session_showGazeCursor"),
                "baseGazeSamples": row.get("session_baseGazeSamples"),
                "dwellSeconds": row.get("session_dwellSeconds"),
                "translations": row.get("session_translations"),
                "uniqueSourceWords": row.get("session_uniqueSourceWords"),
                "translationsPerMinute": row.get("session_translationsPerMinute"),
                "maxTranslationGapSeconds": row.get("session_maxTranslationGapSeconds"),
                "quizDelayAfterSessionMinutes": row.get("quizDelayAfterSessionMinutes"),
                "candidateSessionsForUserDoc": row.get("candidateSessionsForUserDoc"),
                "duplicateQuizResponsesForUserDoc": row.get("duplicateQuizResponsesForUserDoc"),
            }
        )
    write_csv(JOINED_CSV, joined_csv_rows)
    write_csv(USER_SUMMARY_CSV, user_summary_rows(joined, sus_pairs))
    write_csv(SUS_PAIRED_CSV, sus_pairs)
    write_csv(QUESTION_STATS_CSV, qstats)
    write_csv(MISSING_SESSION_REVIEW_CSV, missing_review)
    write_csv(PDF_CONDITION_COMPARISON_CSV, pdf_condition_comparison_rows(joined))

    report = render_report(
        joined,
        unmatched,
        inferred_rows,
        missing_review,
        quiz_responses,
        export_summaries,
        sessions,
        sessions_by_key,
        qstats,
        sus_rows,
        sus_pairs,
        sus_item_cols,
        demographics,
    )
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(REPORT_PATH)
    print(f"db_joined={len(db_joined)} inferred={len(inferred_rows)} usable={len(joined)} unresolved_unmatched={len(unmatched)} sus_pairs={len(sus_pairs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
