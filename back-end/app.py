import io
import uuid
import json
import torch
import asyncio
import sqlite3
import traceback
from flask_cors import CORS
from PyPDF2 import PdfReader
from functools import partial
from datetime import datetime
from config import load_config
from werkzeug.utils import secure_filename
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify, Response
from transformers import MarianMTModel, MarianTokenizer
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

MODELS = {}


def ensure_settings_schema():
    conn = sqlite3.connect(sqLiteDatabase)
    cursor = conn.cursor()
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


ensure_settings_schema()


def get_model(tgt_lang):
    model_key = f'en-{tgt_lang}'

    # Check if GPU/CUDA is available and set the device accordingly
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(device)
    if model_key not in MODELS:
        model_name = f'Helsinki-NLP/opus-mt-en-{tgt_lang}'
        # Load model and tokenizer and move the model to GPU if available
        model = MarianMTModel.from_pretrained(model_name).to(device)
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        MODELS[model_key] = (model, tokenizer)

    return MODELS[model_key]


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
        data = request.json
        text = data['text']
        tgt_lang = data['tgt']

        model, tokenizer = get_model(tgt_lang)

        # Ensuring the input tensors are on the same device as the model
        inputs = tokenizer(text, return_tensors="pt",
                           padding=True).to(model.device)

        outputs = model.generate(**inputs)
        translation = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return jsonify({'translation': translation})

    except Exception as e:
        print(e)  # Logging the error can help in diagnosing the issue
        return jsonify({'error': 'Unable to translate text'}), 500
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
        current = token.get("raw", "").strip()
        if not current:
            continue

        if sentence_parts and current in punctuation_tokens:
            sentence_parts[-1] = sentence_parts[-1].rstrip() + current
        else:
            sentence_parts.append(current)

    return " ".join(sentence_parts).strip()


def _build_sentence_text_with_marker(tokens, marker_idx, start_marker, end_marker):
    sentence_parts = []
    punctuation_tokens = {".", ",", "?", "!", ";", ":"}

    for idx, token in enumerate(tokens):
        current = token.get("raw", "").strip()
        if not current:
            continue

        if (
            marker_idx is not None
            and idx == marker_idx
            and start_marker
            and end_marker
        ):
            current = f"{start_marker} {current} {end_marker}"

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
        start_marker = (data.get('startMarker') or "").strip()
        end_marker = (data.get('endMarker') or "").strip()

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
            sentence_text = matched_token.get("raw", "")

        marker_local_idx = local_match_idx - start
        sentence_with_marker = ""
        if (
            start_marker
            and end_marker
            and 0 <= marker_local_idx < len(sentence_tokens)
        ):
            sentence_with_marker = _build_sentence_text_with_marker(
                sentence_tokens,
                marker_local_idx,
                start_marker,
                end_marker,
            )

        return jsonify({
            "success": True,
            "sentence": sentence_text,
            "sentenceWithMarker": sentence_with_marker,
            "matchedToken": matched_token.get("raw", ""),
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
        return jsonify({'message': 'Username already exists.'}), 400

    password = generate_password_hash(data['password'], method='sha256')

    # Insert without userID; SQLite will auto-assign it
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                   (username, password))
    conn.commit()

    # Get the auto-generated userID if needed
    user_id = cursor.lastrowid

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
        return jsonify({'message': 'Invalid username and password.'}), 400

    if not check_password_hash(user[2], password):
        return jsonify({'message': 'Invalid password.'}), 400

    return jsonify({
        'message': 'Logged in successfully.',
        'username': user[1],
        'userID': user[0]
    }), 200

# ----------------------------- Settings -------------------------------


@app.route('/api/settings', methods=['POST'])
def update_settings():
    data = request.get_json()

    userID = data['userID']
    selected_language = data['language']
    theme = data['theme']
    zoomLevel = data['zoomLevel']
    baseGazeSamples = data.get('baseGazeSamples', 60)
    translationMode = data.get('translationMode', 'word')

    conn = sqlite3.connect(sqLiteDatabase)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_settings WHERE userID = ?", (userID,))
    user_settings = cursor.fetchone()

    if user_settings:
        cursor.execute("UPDATE user_settings SET Selected_language = ?, theme = ?, zoomLevel = ?, baseGazeSamples = ?, translationMode = ? WHERE userID = ?",
                       (selected_language, theme, zoomLevel, baseGazeSamples, translationMode, userID))
    else:
        cursor.execute("INSERT INTO user_settings (userID, Selected_language, theme, zoomLevel, baseGazeSamples, translationMode) VALUES (?, ?, ?, ?, ?, ?)",
                       (userID, selected_language, theme, zoomLevel, baseGazeSamples, translationMode))
    conn.commit()

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
