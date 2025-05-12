# app.py
from flask import Flask, request, jsonify
import easyocr
import numpy as np
import cv2
import base64

app = Flask(__name__)

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)

@app.route('/')
def home():
    return jsonify(message="Send a POST request to /read-text with a base64 image to extract text.")

@app.route('/read-text', methods=['POST'])
def read_text():
    data = request.get_json()

    if not data or 'image_base64' not in data:
        return jsonify(error="No base64 image provided."), 400

    try:
        # Decode base64 image string
        img_data = base64.b64decode(data['image_base64'])
        np_arr = np.frombuffer(img_data, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Run OCR
        results = reader.readtext(image)
        extracted_text = [text for (_, text, _) in results]

        return jsonify(text=extracted_text)

    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
