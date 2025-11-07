import re
import nltk
import websockets
import pytesseract
from PIL import Image
import tobii_research as tr
from config import load_config
from flask import make_response
from nltk.corpus import stopwords
from pdf2image import convert_from_bytes

# --------------------- FUNCTIONS ---------------------------
nltk.download('stopwords')

# Get English stopwords
stop_words = set(stopwords.words('english'))


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin",
                         "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Headers",
                         "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "POST")
    return response


def get_host_and_port(address):
    # Keep IPv4 only..
    hostname = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b|\blocalhost\b', address)
    port = re.search(r':(\d+)', address)
    return hostname.group(), int(port.group(1))


config_data = load_config()
ETSDVM_address = config_data['ETSUIConfig']['ETSDVMport']

# Web socket


async def send_request(request_data):
    server_host, server_port = get_host_and_port(ETSDVM_address)
    async with websockets.connect(f"ws://{server_host}:{server_port}") as websocket:
        # Send the data over the WebSocket connection
        await websocket.send(request_data)
        response_data = await websocket.recv()  # Wait to receive the response
        return response_data

# Word positions


def process_page(page_image):
    words_with_positions = []
    data = pytesseract.image_to_data(
        page_image, output_type=pytesseract.Output.DICT
    )
    words = data['text']
    confidences = data['conf']
    boxes = zip(data['left'], data['top'], data['width'], data['height'])

    for word, confidence, box in zip(words, confidences, boxes):
        if int(confidence) > 30:
            # Remove numbers, symbols, and punctuation
            cleaned_word = re.sub(r'[^a-zA-Z\s]', '', word)

            # Filter words based on length, stop words, acronyms, URLs, and email addresses
            if (len(cleaned_word) > 2 and
                    cleaned_word.lower() not in stop_words and
                    not re.match(r'\b[A-Z]{2,}\b', cleaned_word) and
                    not re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', cleaned_word) and
                    not re.match(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', cleaned_word)):

                words_with_positions.append(
                    {"word": cleaned_word, "confidence": confidence, "box": box}
                )

    return words_with_positions


def resize_pil_image(image, scaling_factor):
    original_width, original_height = image.size
    new_width = int(original_width * scaling_factor)
    new_height = int(original_height * scaling_factor)

    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

    return resized_image


def process_single_page(page_num, pdf_content=None, scaling_factor=1.0, ):
    # Those multipliers are here because of different scaling in the server and the client side.
    final_scale_factor_width = scaling_factor * 1.16951
    final_scale_factor_height = scaling_factor * 1.18566176
    page_images = convert_from_bytes(
        pdf_content, first_page=page_num + 1, last_page=page_num + 1
    )

    if page_images:
        original_image = page_images[0]
        print(original_image.width, original_image.height)
        if scaling_factor != 1:
            scaled_image = original_image.resize(
                (int(original_image.width * final_scale_factor_width),
                 int(original_image.height * final_scale_factor_height)),
                Image.ANTIALIAS
            )

            processed_image = scaled_image
            print(page_num, 'SCALED IMAGE', scaled_image)
        else:
            processed_image = original_image

        return {"page": page_num, "data": process_page(processed_image)}
