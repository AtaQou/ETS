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


@app.route('/api/words-positions', methods=['GET'])
def get_position_of_words():
    try:
        doc_id = request.args.get('docID')
        user_id = request.args.get('userID')
        conn = sqlite3.connect(sqLiteDatabase)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        memo_key = f"{doc_id}_{user_id}"

        # Fetch zoomLevel from user_settings
        c.execute(
            "SELECT zoomLevel FROM user_settings WHERE userID = ?", (user_id,))
        settings_row = c.fetchone()
        if settings_row:
            scaling_factor = settings_row['zoomLevel'] / 1.0
        else:
            scaling_factor = 1.0  # default value
        print(scaling_factor)

        # if (memo_key in memo_object) and (previous_zoom == scaling_factor):
        #     return jsonify({"success": True, "data": memo_object[memo_key]})

        c.execute(
            "SELECT docFile FROM documents WHERE docID = ? AND userID = ?", (doc_id, user_id))
        row = c.fetchone()

        if row:
            pdf_content = row['docFile']
            pdf_reader = PdfReader(io.BytesIO(pdf_content))

            all_pages_data = []

            partial_process_single_page = partial(
                process_single_page, pdf_content=pdf_content, scaling_factor=scaling_factor)

            with ThreadPoolExecutor() as executor:
                all_pages_data = list(executor.map(
                    partial_process_single_page, range(len(pdf_reader.pages))))

            memo_object[memo_key] = all_pages_data

            return jsonify({"success": True, "data": all_pages_data})

        else:
            return jsonify({"success": False, "message": "Document not found"})

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"success": False, "message": "An error occurred"})

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

    conn = sqlite3.connect(sqLiteDatabase)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_settings WHERE userID = ?", (userID,))
    user_settings = cursor.fetchone()

    if user_settings:
        cursor.execute("UPDATE user_settings SET Selected_language = ?, theme = ?, zoomLevel = ?, baseGazeSamples = ? WHERE userID = ?",
                       (selected_language, theme, zoomLevel, baseGazeSamples, userID))
    else:
        cursor.execute("INSERT INTO user_settings (userID, Selected_language, theme, zoomLevel, baseGazeSamples) VALUES (?, ?, ?, ?, ?)",
                       (userID, selected_language, theme, zoomLevel, baseGazeSamples))
    conn.commit()

    return jsonify({'message': 'Settings updated.'}), 200


@app.route('/api/get_settings', methods=['GET'])
def get_user_settings():
    userID = request.args.get('userID')

    # Ensure userID is provided
    if not userID:
        return jsonify({'message': 'userID is required.'}), 400

    conn = sqlite3.connect(sqLiteDatabase)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_settings WHERE userID = ?", (userID,))
    user_settings = cursor.fetchone()

    if not user_settings:
        return jsonify({'message': 'No settings found for this userID.'}), 404

    # Parsing the fetched data into a dictionary
    settings = {
        "userID": user_settings[0],
        "selected_language": user_settings[1],
        "theme": user_settings[2],
        "zoomLevel": user_settings[3],
        "baseGazeSamples": user_settings[4] if len(user_settings) > 4 and user_settings[4] is not None else 60,
    }

    return jsonify(settings), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

