import io
import csv
import uuid
import json
import os
import re
import asyncio
import sqlite3
import requests
import traceback
from flask_cors import CORS
from PyPDF2 import PdfReader
from functools import partial
from datetime import datetime
from config import load_config
from werkzeug.utils import secure_filename
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify, Response
from werkzeug.security import generate_password_hash, check_password_hash

# our utils
from functions import _build_cors_preflight_response, send_request, process_single_page


app = Flask(__name__)
CORS(app, resources={
     r"/api/*": {"origins": ["http://localhost:3000", "http://localhost:3001"]}})
sqLiteDatabase = 'ETSsqLiteDB'

# Load the configuration values from appsettings.json
config_data = load_config()
listening_port = config_data['ETSUIConfig']['ListeningPort']
ETSDVM_address = config_data['ETSUIConfig']['ETSDVMport']
deepl_config = config_data.get('DeepLTranslator', {})
DEEPL_API_KEY = os.getenv(
    "DEEPL_API_KEY",
    deepl_config.get("ApiKey", "")
).strip()
DEEPL_TRANSLATOR_ENDPOINT = os.getenv(
    "DEEPL_TRANSLATOR_ENDPOINT",
    deepl_config.get("Endpoint", "https://api-free.deepl.com/v2/translate")
).strip()
DEEPL_MODEL_TYPE = os.getenv(
    "DEEPL_MODEL_TYPE",
    deepl_config.get("ModelType", "quality_optimized")
).strip()
DEEPL_SPLIT_SENTENCES = os.getenv(
    "DEEPL_SPLIT_SENTENCES",
    str(deepl_config.get("SplitSentences", "0"))
).strip()
try:
    DEEPL_TRANSLATOR_TIMEOUT_SECONDS = int(os.getenv(
        "DEEPL_TRANSLATOR_TIMEOUT_SECONDS",
        str(deepl_config.get("TimeoutSeconds", 12))
    ))
except ValueError:
    DEEPL_TRANSLATOR_TIMEOUT_SECONDS = 12


def ensure_settings_schema():
    conn = sqlite3.connect(sqLiteDatabase)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_settings
        ([userID] INTEGER, [Selected_language] TEXT, [theme] TEXT, [zoomLevel] INTEGER,
         [baseGazeSamples] INTEGER DEFAULT 60, [translationMode] TEXT DEFAULT 'word',
         FOREIGN KEY(userID) REFERENCES users(userID))
    ''')
    cursor.execute("PRAGMA table_info(user_settings)")
    existing_columns = {row[1] for row in cursor.fetchall()}
    if 'baseGazeSamples' not in existing_columns:
        cursor.execute(
            "ALTER TABLE user_settings ADD COLUMN baseGazeSamples INTEGER DEFAULT 60"
        )
        conn.commit()
    if 'translationMode' not in existing_columns:
        cursor.execute(
            "ALTER TABLE user_settings ADD COLUMN translationMode TEXT DEFAULT 'word'"
        )
        conn.commit()
    conn.close()


def ensure_experiment_schema():
    conn = sqlite3.connect(sqLiteDatabase)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions
        ([sessionID] TEXT PRIMARY KEY, [userID] INTEGER NOT NULL, [trackerAddress] TEXT, [trackerName] TEXT,
         [startedAt] DATETIME NOT NULL, [endedAt] DATETIME, [startSettings] TEXT, [endReason] TEXT,
         FOREIGN KEY(userID) REFERENCES users(userID))
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS translation_events
        ([eventID] INTEGER PRIMARY KEY AUTOINCREMENT, [userID] INTEGER NOT NULL, [sessionID] TEXT NOT NULL,
         [docID] INTEGER, [docName] TEXT, [page] INTEGER, [sourceText] TEXT NOT NULL, [translatedText] TEXT NOT NULL,
         [sourceLang] TEXT DEFAULT 'en', [targetLang] TEXT NOT NULL, [translationMode] TEXT DEFAULT 'word',
         [provider] TEXT DEFAULT 'google', [translatedAt] DATETIME NOT NULL, [settingsSnapshot] TEXT,
         [isUndesired] INTEGER NOT NULL DEFAULT 0,
         FOREIGN KEY(userID) REFERENCES users(userID), FOREIGN KEY(sessionID) REFERENCES user_sessions(sessionID))
    ''')
    cursor.execute("PRAGMA table_info(translation_events)")
    translation_columns = {row[1] for row in cursor.fetchall()}
    if 'docName' not in translation_columns:
        cursor.execute("ALTER TABLE translation_events ADD COLUMN docName TEXT")
        conn.commit()
    if 'isUndesired' not in translation_columns:
        cursor.execute("ALTER TABLE translation_events ADD COLUMN isUndesired INTEGER NOT NULL DEFAULT 0")
        conn.commit()
    cursor.execute(
        """
        UPDATE translation_events
        SET docName = (
            SELECT d.docName
            FROM documents d
            WHERE d.docID = translation_events.docID
              AND d.userID = translation_events.userID
            LIMIT 1
        )
        WHERE (docName IS NULL OR TRIM(docName) = '')
          AND docID IS NOT NULL
        """
    )
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS translation_stats
        ([userID] INTEGER NOT NULL, [sessionID] TEXT NOT NULL, [sourceText] TEXT NOT NULL,
         [targetLang] TEXT NOT NULL, [translationMode] TEXT NOT NULL, [usageCount] INTEGER NOT NULL DEFAULT 1,
         [lastTranslation] TEXT, [lastTranslatedAt] DATETIME NOT NULL,
         PRIMARY KEY (userID, sessionID, sourceText, targetLang, translationMode),
         FOREIGN KEY(userID) REFERENCES users(userID), FOREIGN KEY(sessionID) REFERENCES user_sessions(sessionID))
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings_change_events
        ([changeID] INTEGER PRIMARY KEY AUTOINCREMENT, [userID] INTEGER NOT NULL, [sessionID] TEXT,
         [changedFields] TEXT NOT NULL, [oldSettings] TEXT, [newSettings] TEXT NOT NULL, [changedAt] DATETIME NOT NULL,
         FOREIGN KEY(userID) REFERENCES users(userID), FOREIGN KEY(sessionID) REFERENCES user_sessions(sessionID))
    ''')
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_translation_events_user_time ON translation_events(userID, translatedAt DESC)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_translation_events_session_time ON translation_events(sessionID, translatedAt DESC)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_translation_events_user_doc_mode_time ON translation_events(userID, docName, translationMode, translatedAt DESC)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_settings_change_user_time ON settings_change_events(userID, changedAt DESC)"
    )
    conn.commit()
    conn.close()


def ensure_vocabulary_schema():
    conn = sqlite3.connect(sqLiteDatabase)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vocabulary_entries
        ([entryID] INTEGER PRIMARY KEY AUTOINCREMENT, [userID] INTEGER NOT NULL,
         [sourceText] TEXT NOT NULL, [translatedText] TEXT NOT NULL, [translationMode] TEXT NOT NULL DEFAULT 'word',
         [firstTranslatedAt] DATETIME NOT NULL,
         UNIQUE(userID, translationMode, sourceText),
         FOREIGN KEY(userID) REFERENCES users(userID))
    ''')
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_vocabulary_entries_user_mode_time ON vocabulary_entries(userID, translationMode, firstTranslatedAt DESC)"
    )
    conn.commit()
    conn.close()


def _now_iso():
    return datetime.now().isoformat(timespec='seconds')


def _to_json(payload):
    if payload is None:
        return None
    try:
        return json.dumps(payload, ensure_ascii=False)
    except TypeError:
        return json.dumps(str(payload), ensure_ascii=False)


def _from_json(payload):
    if payload is None:
        return None
    try:
        return json.loads(payload)
    except (TypeError, json.JSONDecodeError):
        return payload


def _settings_row_to_dict(row):
    if row is None:
        return None
    return {
        "language": row[1],
        "theme": row[2],
        "zoomLevel": row[3],
        "baseGazeSamples": row[4] if row[4] is not None else 60,
        "translationMode": row[5] if row[5] else "word",
    }


def _get_active_session_id(cursor, user_id):
    cursor.execute(
        "SELECT sessionID FROM user_sessions WHERE userID = ? AND endedAt IS NULL ORDER BY startedAt DESC LIMIT 1",
        (user_id,)
    )
    row = cursor.fetchone()
    if not row:
        return None
    return row[0]


def _get_db_settings(cursor, user_id):
    cursor.execute(
        "SELECT userID, Selected_language, theme, zoomLevel, baseGazeSamples, translationMode FROM user_settings WHERE userID = ?",
        (user_id,)
    )
    return _settings_row_to_dict(cursor.fetchone())


def _to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _is_super_viewer(cursor, user_id):
    parsed_user_id = _to_int(user_id)
    if parsed_user_id is None:
        return False
    cursor.execute("SELECT username FROM users WHERE userID = ?", (parsed_user_id,))
    row = cursor.fetchone()
    if not row or not row[0]:
        return False
    return str(row[0]).strip().casefold() == "sotiris"


def _resolve_requested_user_scope(cursor, requester_user_id, requested_user_id=None):
    requester_id = _to_int(requester_user_id)
    requested_id = _to_int(requested_user_id)
    if requester_id is None and requested_id is not None:
        requester_id = requested_id
    can_view_all = _is_super_viewer(cursor, requester_id)
    if requested_id is not None:
        effective_user_id = requested_id if can_view_all else requester_id
    else:
        effective_user_id = None if can_view_all else requester_id
    return requester_id, effective_user_id, can_view_all


ensure_settings_schema()
ensure_experiment_schema()
ensure_vocabulary_schema()


def _normalize_ocr_token_for_translation(raw_token):
    token = (raw_token or "").strip()
    if not token:
        return token

    # Common OCR confusion: uppercase "I" recognized as vertical bar.
    token = token.replace("¦", "I").replace("ǀ", "I")
    if token == "|":
        return "I"
    if token.startswith("|"):
        return "I" + token[1:]
    return token


def _normalize_text_for_translation(text):
    if not text:
        return text
    return text.replace("¦", "I").replace("ǀ", "I").replace("|", "I")


def _normalize_deepl_language(value, fallback):
    candidate = (value or fallback or "").strip()
    if not candidate:
        return fallback
    normalized = candidate.replace("-", "_").upper()
    # DeepL expects EL for Greek.
    if normalized == "GR":
        return "EL"
    return normalized


def upload_file(file, user_id):
    filename = secure_filename(file.filename)
    file_data = file.read()

    upload_date = datetime.now()

    conn = sqlite3.connect(sqLiteDatabase)
    c = conn.cursor()

    # Check if file with same name and user_id already exists
    c.execute("SELECT COUNT(*) FROM documents WHERE userID = ? AND docName = ?",
              (user_id, filename))
    if c.fetchone()[0] > 0:
        conn.close()
        response = {
            'message': 'File with the same name already exists.',
            'userID': user_id,
            'docName': filename,
        }
        return jsonify(response), 400

    # Make sure user_id is an integer
    user_id = int(user_id)

    # Insert without docID; SQLite will auto-assign it
    c.execute("""
              INSERT INTO documents(userID, docName, docFile, uploadDate, lastReadPage)
              VALUES (?, ?, ?, ?, ?)
              """, (user_id, filename, file_data, upload_date, 0))

    # Get the auto-incremented docID
    new_id = c.lastrowid
    conn.commit()
    conn.close()

    response = {
        'message': 'File uploaded and stored successfully.',
        'docID': new_id,
        'userID': user_id,
        'docName': filename,
        'uploadDate': upload_date.strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(response), 200

# ---------------------- API ROUTES ---------------------------------------


# --------------------------- Translation --------------------------------

@app.route('/api/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json() or {}
        text = _normalize_text_for_translation((data.get('text') or '').strip())
        context = _normalize_text_for_translation((data.get('context') or '').strip())
        mode = (data.get('mode') or data.get('translationMode') or 'word').strip().lower()
        target_lang = _normalize_deepl_language(
            data.get('tgt') or data.get('targetLang'),
            "EL"
        )
        source_lang = _normalize_deepl_language(
            data.get('src') or data.get('sourceLang'),
            "EN"
        )

        if not text:
            return jsonify({'message': 'text is required.'}), 400

        if not DEEPL_API_KEY:
            return jsonify({'message': 'DeepL API key is not configured on the server.'}), 500

        payload = {
            "text": [text],
            "target_lang": target_lang,
            "source_lang": source_lang,
            "preserve_formatting": True,
            "model_type": DEEPL_MODEL_TYPE,
            "split_sentences": DEEPL_SPLIT_SENTENCES,
        }
        if context:
            payload["context"] = context

        response = requests.post(
            DEEPL_TRANSLATOR_ENDPOINT,
            headers={
                "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=DEEPL_TRANSLATOR_TIMEOUT_SECONDS
        )

        if not response.ok:
            try:
                error_payload = response.json()
            except ValueError:
                error_payload = {"raw": response.text}
            print("DeepL translate error:", error_payload)
            return jsonify({
                'message': 'Unable to translate text via DeepL.',
                'details': error_payload
            }), 502

        response_data = response.json() or {}
        translations = response_data.get("translations") or []
        if not translations:
            return jsonify({'message': 'DeepL returned no translations.'}), 502

        translated_text = (translations[0].get("text") or "").strip()
        model_type_used = translations[0].get("model_type_used")

        return jsonify({
            'translation': translated_text,
            'provider': 'deepl',
            'mode': mode,
            'sourceText': text,
            'contextUsed': bool(context),
            'modelTypeRequested': DEEPL_MODEL_TYPE,
            'modelTypeUsed': model_type_used,
        }), 200

    except Exception:
        print(traceback.format_exc())
        return jsonify({'message': 'Unable to translate text'}), 500
# --------------------------- Files --------------------------------


@app.route('/api/get_file', methods=['GET'])
def get_file():
    doc_id = request.args.get('docID')
    user_id = request.args.get('userID')
    if doc_id is None:
        return "No docID provided", 400

    conn = sqlite3.connect(sqLiteDatabase)
    c = conn.cursor()

    c.execute("SELECT * FROM documents WHERE docID = ? AND userID = ?",
              (doc_id, user_id))
    record = c.fetchone()

    if record is None:
        conn.close()
        return "No record found with the provided docID", 404

    conn.close()

    file_data = record[3]
    file_object = io.BytesIO(file_data)
    file_name = record[2]

    return Response(file_object, mimetype='application/pdf',
                    headers={"Content-Disposition": f"attachment;filename={file_name}"})


@app.route('/api/upload_file', methods=['POST'])
def parse_file():
    print(request.form)  # Debugging line
    user_id = int(request.form.get('userID', 1))
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400
    if file:
        print('file', file)
        response = upload_file(file, user_id)
        return response
    else:
        return "Allowed file type only.", 415


@app.route('/api/delete_file', methods=['DELETE'])
def delete_file():
    doc_id = request.args.get('docID')
    user_id = request.args.get('userID')

    if not doc_id:
        return "docID required", 400

    # Assumes remove_file function does the deletion logic
    response = remove_file(doc_id, user_id)
    return response


def remove_file(doc_id, user_id):
    # Logic to remove the file metadata from the database based on doc_id and user_id

    conn = sqlite3.connect(sqLiteDatabase)
    c = conn.cursor()

    # Check if the file with given doc_id and user_id exists
    c.execute("SELECT COUNT(*), docName FROM documents WHERE docID = ? AND userID = ?",
              (doc_id, user_id))
    row = c.fetchone()

    if row[0] == 0:
        conn.close()
        response = {
            'message': 'File not found or unauthorized.',
            'docID': doc_id,
            'userID': user_id
        }
        return jsonify(response), 404

    c.execute("DELETE FROM documents WHERE docID = ? AND userID = ?",
              (doc_id, user_id))
    conn.commit()
    conn.close()

    response = {
        'message': 'File deleted successfully.',
        'docID': doc_id,
        'userID': user_id
    }
    return jsonify(response), 200


@app.route('/api/documents', methods=['GET'])
def get_documents():
    try:
        user_id = request.args.get('userID')

        conn = sqlite3.connect(sqLiteDatabase)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute(
            "SELECT docID, userID, docName, uploadDate, lastReadPage FROM documents WHERE userID=?", (user_id,))

        documents = c.fetchall()
        print(documents)
        documents_list = [dict(row) for row in documents]
        print(documents_list)
        return jsonify(documents_list)
    except Exception as e:
        print(traceback.format_exc())  # This will print the full traceback
        return jsonify({"error": str(e)}), 500


# --------------------------- Words positions --------------------------------

memo_object = {}


def _get_user_scaling_factor(cursor, user_id):
    cursor.execute(
        "SELECT zoomLevel FROM user_settings WHERE userID = ?", (user_id,))
    settings_row = cursor.fetchone()
    if settings_row:
        zoom_level = settings_row['zoomLevel']
        if zoom_level is None:
            return 1.0
        return float(zoom_level)
    return 1.0


def _build_pages_data(pdf_content, scaling_factor):
    pdf_reader = PdfReader(io.BytesIO(pdf_content))
    partial_process_single_page = partial(
        process_single_page, pdf_content=pdf_content, scaling_factor=scaling_factor)
    with ThreadPoolExecutor() as executor:
        return list(executor.map(partial_process_single_page, range(len(pdf_reader.pages))))


def _find_focus_token(tokens, focus_box):
    fx, fy, fw, fh = focus_box
    f_right = fx + fw
    f_bottom = fy + fh

    best_idx = None
    best_score = -1.0

    for idx, token in enumerate(tokens):
        tx, ty, tw, th = token.get("box", [0, 0, 0, 0])
        t_right = tx + tw
        t_bottom = ty + th

        inter_w = max(0, min(f_right, t_right) - max(fx, tx))
        inter_h = max(0, min(f_bottom, t_bottom) - max(fy, ty))
        inter_area = inter_w * inter_h
        if inter_area <= 0:
            continue

        token_area = max(1, tw * th)
        score = inter_area / token_area
        if score > best_score:
            best_score = score
            best_idx = idx

    return best_idx


def _is_sentence_boundary(raw_token):
    return any(ch in raw_token for ch in ".?!,")


def _build_sentence_text(tokens):
    sentence_parts = []
    punctuation_tokens = {".", ",", "?", "!", ";", ":"}
    for token in tokens:
        current = _normalize_ocr_token_for_translation(token.get("raw", ""))
        if not current:
            continue

        if sentence_parts and current in punctuation_tokens:
            sentence_parts[-1] = sentence_parts[-1].rstrip() + current
        else:
            sentence_parts.append(current)

    return " ".join(sentence_parts).strip()


@app.route('/api/words-positions', methods=['GET'])
def get_position_of_words():
    try:
        doc_id = request.args.get('docID')
        user_id = request.args.get('userID')
        conn = sqlite3.connect(sqLiteDatabase)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        memo_key = f"{doc_id}_{user_id}"

        scaling_factor = _get_user_scaling_factor(c, user_id)
        print(scaling_factor)

        memo_key = f"{memo_key}_{round(scaling_factor, 4)}"
        if memo_key in memo_object:
            return jsonify({"success": True, "data": memo_object[memo_key]})

        c.execute(
            "SELECT docFile FROM documents WHERE docID = ? AND userID = ?", (doc_id, user_id))
        row = c.fetchone()

        if row:
            pdf_content = row['docFile']
            all_pages_data = _build_pages_data(pdf_content, scaling_factor)

            memo_object[memo_key] = all_pages_data

            return jsonify({"success": True, "data": all_pages_data})

        else:
            return jsonify({"success": False, "message": "Document not found"})

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"success": False, "message": "An error occurred"})


@app.route('/api/sentence-from-focus', methods=['POST'])
def sentence_from_focus():
    try:
        data = request.get_json()
        doc_id = data.get('docID')
        user_id = data.get('userID')
        page = data.get('page')
        focus_box = data.get('focusBox')

        if doc_id is None or user_id is None or page is None or not focus_box:
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        conn = sqlite3.connect(sqLiteDatabase)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        scaling_factor = _get_user_scaling_factor(c, user_id)
        memo_key = f"{doc_id}_{user_id}_{round(scaling_factor, 4)}"
        pages_data = memo_object.get(memo_key)

        if pages_data is None:
            c.execute(
                "SELECT docFile FROM documents WHERE docID = ? AND userID = ?", (doc_id, user_id))
            row = c.fetchone()
            if not row:
                conn.close()
                return jsonify({"success": False, "message": "Document not found"}), 404
            pages_data = _build_pages_data(row['docFile'], scaling_factor)
            memo_object[memo_key] = pages_data

        conn.close()

        page_index = int(page) - 1
        if page_index < 0 or page_index >= len(pages_data):
            return jsonify({"success": False, "message": "Invalid page"}), 400

        page_data = pages_data[page_index]
        tokens = page_data.get("tokensAll", [])
        if not tokens:
            return jsonify({"success": False, "message": "No OCR tokens on page"}), 404

        matched_idx = _find_focus_token(tokens, focus_box)
        if matched_idx is None:
            return jsonify({"success": False, "message": "No matching token found"}), 404

        matched_token = tokens[matched_idx]
        matched_token_raw = matched_token.get("raw", "")
        matched_token_normalized = _normalize_ocr_token_for_translation(matched_token_raw)
        scoped_tokens = [
            token for token in tokens
            if token.get("block_num") == matched_token.get("block_num")
            and token.get("par_num") == matched_token.get("par_num")
        ]
        if len(scoped_tokens) < 2:
            scoped_tokens = tokens

        local_match_idx = _find_focus_token(scoped_tokens, focus_box)
        if local_match_idx is None:
            return jsonify({"success": False, "message": "No matching token found"}), 404

        start = local_match_idx
        while start > 0 and not _is_sentence_boundary(scoped_tokens[start - 1].get("raw", "")):
            start -= 1

        end = local_match_idx
        while end < len(scoped_tokens) - 1 and not _is_sentence_boundary(scoped_tokens[end].get("raw", "")):
            end += 1

        sentence_tokens = scoped_tokens[start:end + 1]
        sentence_text = _build_sentence_text(sentence_tokens)
        if not sentence_text:
            sentence_text = matched_token_normalized

        return jsonify({
            "success": True,
            "sentence": sentence_text,
            "matchedToken": matched_token_normalized,
            "matchedTokenRaw": matched_token_raw,
        }), 200
    except Exception:
        print(traceback.format_exc())
        return jsonify({"success": False, "message": "An error occurred"}), 500

# ---------------------- Eye tracker ----------------------------


@app.route('/api/search', methods=['POST'])
def search_eye_tracker():
    request_data = {
        "action": "search_eye_tracker"
    }

    # Convert the dictionary to a JSON string for sending the request
    request_json = json.dumps(request_data)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response_data = loop.run_until_complete(send_request(request_json))

    # Convert JSON string to a Python dictionary or list. The returned type of response_data must be string.
    return json.loads(response_data)


@app.route('/api/connect', methods=['POST'])
def get_eye_tracker():
    data = request.get_json()

    address = data['address']
    print("I arrived: ", address)
    request_data = {
        "action": "connect_to_tracker",
        "address": address
    }
    request_json = json.dumps(request_data)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response_data = loop.run_until_complete(send_request(request_json))

    try:
        response_dict = json.loads(response_data)
        message = response_dict.get('message', 'Unknown status')
    except json.JSONDecodeError:
        message = 'Invalid response format'

    return jsonify({"message": message}), 200


# ----------------------------- Session + Logs ------------------------------------


@app.route('/api/session/start', methods=['POST'])
def start_session():
    data = request.get_json() or {}
    user_id = data.get('userID')
    if not user_id:
        return jsonify({'message': 'userID is required.'}), 400

    tracker_address = data.get('trackerAddress')
    tracker_name = data.get('trackerName')
    start_settings = data.get('settings')
    started_at = _now_iso()
    session_id = str(uuid.uuid4())

    conn = sqlite3.connect(sqLiteDatabase)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE user_sessions SET endedAt = ?, endReason = ? WHERE userID = ? AND endedAt IS NULL",
            (started_at, 'replaced_by_new_session', user_id)
        )

        if start_settings is None:
            start_settings = _get_db_settings(cursor, user_id)

        cursor.execute(
            """INSERT INTO user_sessions(sessionID, userID, trackerAddress, trackerName, startedAt, startSettings)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (session_id, user_id, tracker_address, tracker_name, started_at, _to_json(start_settings))
        )
        conn.commit()
    except Exception:
        conn.rollback()
        print(traceback.format_exc())
        return jsonify({'message': 'Unable to start session.'}), 500
    finally:
        conn.close()

    return jsonify({
        'message': 'Session started.',
        'sessionID': session_id,
        'startedAt': started_at
    }), 200


@app.route('/api/session/end', methods=['POST'])
def end_session():
    data = request.get_json() or {}
    user_id = data.get('userID')
    session_id = data.get('sessionID')
    reason = data.get('reason', 'manual_disconnect')
    ended_at = _now_iso()

    if not user_id:
        return jsonify({'message': 'userID is required.'}), 400

    conn = sqlite3.connect(sqLiteDatabase)
    cursor = conn.cursor()

    try:
        if not session_id:
            session_id = _get_active_session_id(cursor, user_id)

        if not session_id:
            return jsonify({'message': 'No active session found.'}), 200

        cursor.execute(
            """UPDATE user_sessions
               SET endedAt = COALESCE(endedAt, ?), endReason = COALESCE(endReason, ?)
               WHERE sessionID = ? AND userID = ?""",
            (ended_at, reason, session_id, user_id)
        )
        conn.commit()
    except Exception:
        conn.rollback()
        print(traceback.format_exc())
        return jsonify({'message': 'Unable to end session.'}), 500
    finally:
        conn.close()

    return jsonify({
        'message': 'Session closed.',
        'sessionID': session_id,
        'endedAt': ended_at
    }), 200


@app.route('/api/log-translation', methods=['POST'])
def log_translation_event():
    data = request.get_json() or {}

    user_id = data.get('userID')
    session_id = data.get('sessionID')
    source_text = (data.get('sourceText') or '').strip()
    translated_text = (data.get('translatedText') or '').strip()
    source_lang = data.get('sourceLang', 'en')
    target_lang = data.get('targetLang', 'el')
    translation_mode = (data.get('translationMode') or 'word').strip().lower()
    if translation_mode not in ('word', 'sentence'):
        translation_mode = 'word'
    provider = data.get('provider', 'google')
    doc_id = data.get('docID')
    doc_name = (data.get('docName') or '').strip()
    page = data.get('page')
    translated_at = data.get('translatedAt') or _now_iso()
    settings_snapshot = data.get('settings')
    is_undesired = 1 if data.get('isUndesired') else 0

    if not user_id:
        return jsonify({'message': 'userID is required.'}), 400
    if not source_text or not translated_text:
        return jsonify({'message': 'sourceText and translatedText are required.'}), 400

    conn = sqlite3.connect(sqLiteDatabase)
    cursor = conn.cursor()

    try:
        if not session_id:
            session_id = _get_active_session_id(cursor, user_id)

        if not session_id:
            return jsonify({'message': 'No active session for this user.'}), 400

        cursor.execute(
            "SELECT sessionID FROM user_sessions WHERE sessionID = ? AND userID = ? AND endedAt IS NULL",
            (session_id, user_id)
        )
        active_session = cursor.fetchone()
        if not active_session:
            return jsonify({'message': 'Session is not active.'}), 400

        if settings_snapshot is None:
            settings_snapshot = _get_db_settings(cursor, user_id)

        if not doc_name and doc_id is not None:
            cursor.execute(
                "SELECT docName FROM documents WHERE docID = ? AND userID = ?",
                (doc_id, user_id)
            )
            doc_row = cursor.fetchone()
            if doc_row and doc_row[0]:
                doc_name = doc_row[0]

        if isinstance(settings_snapshot, dict):
            settings_snapshot = {
                **settings_snapshot,
                "currentPdfFile": doc_name or None,
            }

        cursor.execute(
            """INSERT INTO translation_events(
                userID, sessionID, docID, docName, page, sourceText, translatedText,
                sourceLang, targetLang, translationMode, provider, translatedAt, settingsSnapshot, isUndesired
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user_id, session_id, doc_id, doc_name or None, page, source_text, translated_text,
                source_lang, target_lang, translation_mode, provider, translated_at, _to_json(settings_snapshot), is_undesired
            )
        )
        event_id = cursor.lastrowid

        cursor.execute(
            """INSERT INTO translation_stats(
                userID, sessionID, sourceText, targetLang, translationMode, usageCount, lastTranslation, lastTranslatedAt
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(userID, sessionID, sourceText, targetLang, translationMode)
            DO UPDATE SET
                usageCount = usageCount + 1,
                lastTranslation = excluded.lastTranslation,
                lastTranslatedAt = excluded.lastTranslatedAt""",
            (user_id, session_id, source_text, target_lang, translation_mode, 1, translated_text, translated_at)
        )

        conn.commit()
    except Exception:
        conn.rollback()
        print(traceback.format_exc())
        return jsonify({'message': 'Unable to log translation.'}), 500
    finally:
        conn.close()

    return jsonify({'message': 'Translation event logged.', 'eventID': event_id}), 200


@app.route('/api/translation-feedback', methods=['POST'])
def update_translation_feedback():
    data = request.get_json() or {}
    event_id = _to_int(data.get('eventID'))
    user_id = _to_int(data.get('userID'))
    is_undesired = 1 if data.get('isUndesired') else 0

    if event_id is None:
        return jsonify({'message': 'eventID is required.'}), 400
    if user_id is None:
        return jsonify({'message': 'userID is required.'}), 400

    conn = sqlite3.connect(sqLiteDatabase)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE translation_events SET isUndesired = ? WHERE eventID = ? AND userID = ?",
            (is_undesired, event_id, user_id)
        )
        if cursor.rowcount == 0:
            return jsonify({'message': 'Translation event not found.'}), 404
        conn.commit()
    except Exception:
        conn.rollback()
        print(traceback.format_exc())
        return jsonify({'message': 'Unable to update translation feedback.'}), 500
    finally:
        conn.close()

    return jsonify({'message': 'Translation feedback saved.'}), 200


@app.route('/api/vocabulary', methods=['GET'])
def get_vocabulary():
    requested_user_id = request.args.get('userID')
    requester_user_id = request.args.get('requesterUserID')
    selected_doc_name = (request.args.get('docName') or '').strip()

    conn = sqlite3.connect(sqLiteDatabase)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        requester_id, effective_user_id, can_view_all = _resolve_requested_user_scope(
            cursor,
            requester_user_id,
            requested_user_id
        )
        if requester_id is None:
            return jsonify({'message': 'requesterUserID is required.'}), 400
        if effective_user_id is None:
            effective_user_id = requester_id

        cursor.execute(
            """
            WITH translation_rows AS (
                SELECT
                    e.eventID,
                    e.userID,
                    e.sourceText,
                    e.translatedText,
                    e.translationMode,
                    e.translatedAt,
                    e.docID,
                    COALESCE(NULLIF(TRIM(e.docName), ''), d.docName, '') AS docName
                FROM translation_events e
                LEFT JOIN documents d
                    ON d.docID = e.docID AND d.userID = e.userID
                WHERE e.userID = ?
                  AND COALESCE(e.isUndesired, 0) = 0
                  AND (? = '' OR COALESCE(NULLIF(TRIM(e.docName), ''), d.docName, '') = ?)
            ),
            ranked AS (
                SELECT
                    eventID,
                    userID,
                    sourceText,
                    translatedText,
                    translationMode,
                    translatedAt AS firstTranslatedAt,
                    docID,
                    docName,
                    ROW_NUMBER() OVER (
                        PARTITION BY translationMode, LOWER(TRIM(sourceText))
                        ORDER BY translatedAt ASC, eventID ASC
                    ) AS rowRank
                FROM translation_rows
            )
            SELECT
                eventID AS entryID,
                userID,
                sourceText,
                translatedText,
                translationMode,
                firstTranslatedAt,
                docID,
                docName
            FROM ranked
            WHERE rowRank = 1
            ORDER BY firstTranslatedAt DESC
            """,
            (effective_user_id, selected_doc_name, selected_doc_name)
        )
        rows = [dict(row) for row in cursor.fetchall()]

        cursor.execute(
            """
            SELECT DISTINCT COALESCE(NULLIF(TRIM(e.docName), ''), d.docName, '') AS docName
            FROM translation_events e
            LEFT JOIN documents d
                ON d.docID = e.docID AND d.userID = e.userID
            WHERE e.userID = ?
              AND COALESCE(e.isUndesired, 0) = 0
              AND COALESCE(NULLIF(TRIM(e.docName), ''), d.docName, '') <> ''
            ORDER BY docName ASC
            """,
            (effective_user_id,)
        )
        doc_names = [row["docName"] for row in cursor.fetchall() if row["docName"]]
    except Exception:
        print(traceback.format_exc())
        return jsonify({'message': 'Unable to fetch vocabulary.'}), 500
    finally:
        conn.close()

    vocabulary = {
        'word': [row for row in rows if row.get('translationMode') == 'word'],
        'sentence': [row for row in rows if row.get('translationMode') == 'sentence'],
        'documents': doc_names,
        'effectiveUserID': effective_user_id,
        'canViewAllUsers': can_view_all,
    }
    return jsonify(vocabulary), 200


@app.route('/api/experiment/sessions', methods=['GET'])
def get_experiment_sessions():
    requested_user_id = request.args.get('userID')
    requester_user_id = request.args.get('requesterUserID')
    conn = sqlite3.connect(sqLiteDatabase)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        requester_id, effective_user_id, _can_view_all = _resolve_requested_user_scope(
            cursor,
            requester_user_id,
            requested_user_id
        )
        if requester_id is None:
            return jsonify({'message': 'requesterUserID is required.'}), 400

        query = """
            SELECT
                s.sessionID, s.userID, u.username, s.trackerAddress, s.trackerName,
                s.startedAt, s.endedAt, s.endReason, s.startSettings,
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
        """
        params = []
        if effective_user_id is not None:
            query += " WHERE s.userID = ?"
            params.append(effective_user_id)
        query += " ORDER BY s.startedAt DESC"
        cursor.execute(query, params)
        sessions = [dict(row) for row in cursor.fetchall()]
        for row in sessions:
            row['startSettings'] = _from_json(row.get('startSettings'))
    except Exception:
        print(traceback.format_exc())
        return jsonify({'message': 'Unable to fetch sessions.'}), 500
    finally:
        conn.close()

    return jsonify(sessions), 200


@app.route('/api/experiment/users', methods=['GET'])
def get_experiment_users():
    requester_user_id = request.args.get('requesterUserID')
    conn = sqlite3.connect(sqLiteDatabase)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        requester_id, _effective_user_id, can_view_all = _resolve_requested_user_scope(
            cursor,
            requester_user_id,
            None
        )
        if requester_id is None:
            return jsonify({'message': 'requesterUserID is required.'}), 400

        query = """
            SELECT
                u.userID,
                u.username,
                COALESCE(s.sessionCount, 0) AS sessionCount,
                COALESCE(t.translationCount, 0) AS translationCount
            FROM users u
            LEFT JOIN (
                SELECT userID, COUNT(*) AS sessionCount
                FROM user_sessions
                GROUP BY userID
            ) s ON s.userID = u.userID
            LEFT JOIN (
                SELECT userID, COUNT(*) AS translationCount
                FROM translation_events
                GROUP BY userID
            ) t ON t.userID = u.userID
        """
        params = []
        if not can_view_all:
            query += " WHERE u.userID = ?"
            params.append(requester_id)
        query += " ORDER BY u.userID ASC"
        cursor.execute(query, params)
        users = [dict(row) for row in cursor.fetchall()]
    except Exception:
        print(traceback.format_exc())
        return jsonify({'message': 'Unable to fetch users.'}), 500
    finally:
        conn.close()

    return jsonify(users), 200


@app.route('/api/experiment/translations', methods=['GET'])
def get_experiment_translations():
    requested_user_id = request.args.get('userID')
    requester_user_id = request.args.get('requesterUserID')
    session_id = request.args.get('sessionID')
    raw_limit = request.args.get('limit', '2000')
    try:
        limit = min(max(int(raw_limit), 1), 10000)
    except ValueError:
        limit = 2000

    conn = sqlite3.connect(sqLiteDatabase)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        requester_id, effective_user_id, _can_view_all = _resolve_requested_user_scope(
            cursor,
            requester_user_id,
            requested_user_id
        )
        if requester_id is None:
            return jsonify({'message': 'requesterUserID is required.'}), 400

        query = """
            SELECT eventID, userID, sessionID, docID, docName, page, sourceText, translatedText,
                   sourceLang, targetLang, translationMode, provider, translatedAt, settingsSnapshot
                   , COALESCE(isUndesired, 0) AS isUndesired
            FROM translation_events
            WHERE 1 = 1
        """
        params = []
        if effective_user_id is not None:
            query += " AND userID = ?"
            params.append(effective_user_id)
        if session_id:
            query += " AND sessionID = ?"
            params.append(session_id)
        query += " ORDER BY translatedAt DESC LIMIT ?"
        params.append(limit)
        cursor.execute(query, params)
        events = [dict(row) for row in cursor.fetchall()]
        for row in events:
            row['settingsSnapshot'] = _from_json(row.get('settingsSnapshot'))
    except Exception:
        print(traceback.format_exc())
        return jsonify({'message': 'Unable to fetch translation events.'}), 500
    finally:
        conn.close()

    return jsonify(events), 200


@app.route('/api/experiment/settings-changes', methods=['GET'])
def get_experiment_settings_changes():
    requested_user_id = request.args.get('userID')
    requester_user_id = request.args.get('requesterUserID')
    session_id = request.args.get('sessionID')

    conn = sqlite3.connect(sqLiteDatabase)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        requester_id, effective_user_id, _can_view_all = _resolve_requested_user_scope(
            cursor,
            requester_user_id,
            requested_user_id
        )
        if requester_id is None:
            return jsonify({'message': 'requesterUserID is required.'}), 400

        query = """
            SELECT changeID, userID, sessionID, changedFields, oldSettings, newSettings, changedAt
            FROM settings_change_events
            WHERE 1 = 1
        """
        params = []
        if effective_user_id is not None:
            query += " AND userID = ?"
            params.append(effective_user_id)
        if session_id:
            query += " AND sessionID = ?"
            params.append(session_id)
        query += " ORDER BY changedAt DESC"
        cursor.execute(query, params)
        events = [dict(row) for row in cursor.fetchall()]
        for row in events:
            row['changedFields'] = _from_json(row.get('changedFields')) or []
            row['oldSettings'] = _from_json(row.get('oldSettings'))
            row['newSettings'] = _from_json(row.get('newSettings'))
    except Exception:
        print(traceback.format_exc())
        return jsonify({'message': 'Unable to fetch settings changes.'}), 500
    finally:
        conn.close()

    return jsonify(events), 200


@app.route('/api/experiment/export', methods=['GET'])
def export_experiment_data():
    requested_user_id = request.args.get('userID')
    requester_user_id = request.args.get('requesterUserID')
    session_id = request.args.get('sessionID')

    conn = sqlite3.connect(sqLiteDatabase)
    cursor = conn.cursor()

    try:
        requester_id, effective_user_id, _can_view_all = _resolve_requested_user_scope(
            cursor,
            requester_user_id,
            requested_user_id
        )
        if requester_id is None:
            return jsonify({'message': 'requesterUserID is required.'}), 400

        query = """
            SELECT
                e.eventID, e.userID, u.username, e.sessionID,
                s.startedAt AS sessionStartedAt, s.endedAt AS sessionEndedAt,
                e.docID, e.docName, e.page, e.sourceText, e.translatedText,
                e.sourceLang, e.targetLang, e.translationMode, e.provider, e.translatedAt,
                COALESCE(e.isUndesired, 0) AS isUndesired
            FROM translation_events e
            LEFT JOIN users u ON u.userID = e.userID
            LEFT JOIN user_sessions s ON s.sessionID = e.sessionID
            WHERE 1 = 1
        """
        params = []
        if effective_user_id is not None:
            query += " AND e.userID = ?"
            params.append(effective_user_id)
        if session_id:
            query += " AND e.sessionID = ?"
            params.append(session_id)
        query += " ORDER BY e.translatedAt DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
    except Exception:
        print(traceback.format_exc())
        return jsonify({'message': 'Unable to export experiment data.'}), 500
    finally:
        conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "eventID", "userID", "username", "sessionID", "sessionStartedAt",
        "sessionEndedAt", "docID", "docName", "page", "sourceText", "translatedText",
        "sourceLang", "targetLang", "translationMode", "provider", "translatedAt", "isUndesired"
    ])
    for row in rows:
        writer.writerow(row)

    filename = f"experiment_translations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


# -----------------------------User profile------------------------------------


@app.route('/api/create-profile', methods=['POST'])
def create_profile():
    data = request.get_json()

    username = data['username']

    if len(username) < 6:
        return jsonify({'message': 'Username should be at least 6 characters.'}), 400

    if len(data['password']) < 6:
        return jsonify({'message': 'Password should be at least 6 characters.'}), 400

    conn = sqlite3.connect(sqLiteDatabase)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    print(user)

    if user:
        conn.close()
        return jsonify({'message': 'Username already exists.'}), 400

    password = generate_password_hash(data['password'], method='sha256')

    # Insert without userID; SQLite will auto-assign it
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                   (username, password))
    conn.commit()

    # Get the auto-generated userID if needed
    user_id = cursor.lastrowid
    conn.close()

    return jsonify({'message': 'New user created.', 'userID': user_id}), 200


@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    data = request.get_json()

    username = data['username']
    password = data['password']

    conn = sqlite3.connect(sqLiteDatabase)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if user is None:
        conn.close()
        return jsonify({'message': 'Invalid username and password.'}), 400

    if not check_password_hash(user[2], password):
        conn.close()
        return jsonify({'message': 'Invalid password.'}), 400

    active_session_id = _get_active_session_id(cursor, user[0])
    conn.close()

    return jsonify({
        'message': 'Logged in successfully.',
        'username': user[1],
        'userID': user[0],
        'sessionID': active_session_id or ""
    }), 200

# ----------------------------- Settings -------------------------------


@app.route('/api/settings', methods=['POST'])
def update_settings():
    data = request.get_json()

    userID = data['userID']
    selected_language = data['language']
    theme = data['theme']
    zoomLevel = data['zoomLevel']
    baseGazeSamples = _to_int(data.get('baseGazeSamples', 60))
    if baseGazeSamples is None:
        baseGazeSamples = 60
    baseGazeSamples = max(1, min(1200, baseGazeSamples))
    translationMode = data.get('translationMode', 'word')
    sessionID = data.get('sessionID')

    conn = sqlite3.connect(sqLiteDatabase)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT userID, Selected_language, theme, zoomLevel, baseGazeSamples, translationMode FROM user_settings WHERE userID = ?",
        (userID,)
    )
    user_settings_row = cursor.fetchone()
    old_settings = _settings_row_to_dict(user_settings_row)

    new_settings = {
        "language": selected_language,
        "theme": theme,
        "zoomLevel": zoomLevel,
        "baseGazeSamples": baseGazeSamples,
        "translationMode": translationMode,
    }
    changed_fields = []
    if old_settings is None:
        changed_fields = list(new_settings.keys())
    else:
        changed_fields = [
            key for key in new_settings.keys()
            if old_settings.get(key) != new_settings.get(key)
        ]

    if user_settings_row:
        cursor.execute("UPDATE user_settings SET Selected_language = ?, theme = ?, zoomLevel = ?, baseGazeSamples = ?, translationMode = ? WHERE userID = ?",
                       (selected_language, theme, zoomLevel, baseGazeSamples, translationMode, userID))
    else:
        cursor.execute("INSERT INTO user_settings (userID, Selected_language, theme, zoomLevel, baseGazeSamples, translationMode) VALUES (?, ?, ?, ?, ?, ?)",
                       (userID, selected_language, theme, zoomLevel, baseGazeSamples, translationMode))

    if changed_fields:
        if not sessionID:
            sessionID = _get_active_session_id(cursor, userID)
        cursor.execute(
            """INSERT INTO settings_change_events(
                userID, sessionID, changedFields, oldSettings, newSettings, changedAt
            ) VALUES (?, ?, ?, ?, ?, ?)""",
            (userID, sessionID, _to_json(changed_fields), _to_json(old_settings), _to_json(new_settings), _now_iso())
        )

    conn.commit()
    conn.close()

    return jsonify({'message': 'Settings updated.'}), 200


@app.route('/api/get_settings', methods=['GET'])
def get_user_settings():
    userID = request.args.get('userID')

    # Ensure userID is provided
    if not userID:
        return jsonify({'message': 'userID is required.'}), 400

    conn = sqlite3.connect(sqLiteDatabase)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT userID, Selected_language, theme, zoomLevel, baseGazeSamples, translationMode FROM user_settings WHERE userID = ?", (userID,))
    user_settings = cursor.fetchone()

    if not user_settings:
        return jsonify({'message': 'No settings found for this userID.'}), 404

    # Parsing the fetched data into a dictionary
    settings = {
        "userID": user_settings["userID"],
        "selected_language": user_settings["Selected_language"],
        "theme": user_settings["theme"],
        "zoomLevel": user_settings["zoomLevel"],
        "baseGazeSamples": user_settings["baseGazeSamples"] if user_settings["baseGazeSamples"] is not None else 60,
        "translationMode": user_settings["translationMode"] if user_settings["translationMode"] else "word",
    }

    return jsonify(settings), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
