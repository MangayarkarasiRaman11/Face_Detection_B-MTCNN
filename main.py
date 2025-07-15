from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
from mtcnn import MTCNN
import os
import uuid

app = Flask(__name__)

# Directory for storing uploaded images
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def detect_faces(image_path, method):
    """Detect faces using either MTCNN or B-MTCNN"""
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    detector = MTCNN()
    faces = detector.detect_faces(image_rgb)

    if not faces:
        return None  # No faces detected

    for face in faces:
        x, y, width, height = face['box']
        confidence = face['confidence']
        keypoints = face['keypoints']

        # Extra facial keypoints for B-MTCNN
        if method == "B-MTCNN":
            keypoints["right_cheek"] = (x + int(0.8 * width), y + int(0.6 * height))
            keypoints["left_cheek"] = (x + int(0.2 * width), y + int(0.6 * height))
            keypoints["forehead_top"] = (x + int(0.5 * width), y + int(0.1 * height))
            keypoints["forehead_mid"] = (x + int(0.5 * width), y + int(0.2 * height))
            keypoints["forehead_bottom"] = (x + int(0.5 * width), y + int(0.3 * height))
            keypoints["right_mouth_corner"] = (x + int(0.8 * width), y + int(0.85 * height))
            keypoints["left_mouth_corner"] = (x + int(0.2 * width), y + int(0.85 * height))

        # Select colors for bounding box and text
        rect_color = (0, 255, 0) if method == "MTCNN" else (255, 0, 0)
        text_bg_color = (255, 255, 0) if method == "MTCNN" else (255, 200, 0)

        # Draw bounding box
        cv2.rectangle(image, (x, y), (x + width, y + height), rect_color, 2)

        # Draw confidence score
        cv2.rectangle(image, (x, y - 20), (x + 60, y), text_bg_color, -1)
        cv2.putText(image, f"{confidence:.4f}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        # Draw facial keypoints
        for key, point in keypoints.items():
            if method == "B-MTCNN" and key in ["right_cheek", "left_cheek", "forehead_top", "forehead_mid", "forehead_bottom", "right_mouth_corner", "left_mouth_corner"]:
                landmark_color = (0, 0, 255)  # Red for extra B-MTCNN points
            else:
                landmark_color = (255, 165, 0) if method == "MTCNN" else (0, 165, 255)

            cv2.circle(image, point, 3, landmark_color, -1)

    # Save processed image
    result_filename = f"result_{uuid.uuid4().hex}.jpg"
    result_path = os.path.join(UPLOAD_FOLDER, result_filename)
    cv2.imwrite(result_path, image)
    return result_filename

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/detect')
def detect_page():
    return render_template('index.html')

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/detect', methods=['POST'])
def detect():
    """Handle file upload and run face detection"""
    if 'image' not in request.files:
        return "No file uploaded!"

    file = request.files['image']
    if file.filename == '':
        return "No selected file!"

    method = request.form.get('method')  # Get selected method (MTCNN or B-MTCNN)

    # Save the uploaded file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Call detect_faces function with correct parameters
    result_filename = detect_faces(filepath, method)

    if not result_filename:
        return "No faces detected! Try another image."

    result_url = url_for('static', filename=f'uploads/{result_filename}')

    return render_template('result.html', result_image=result_url, method=method)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
