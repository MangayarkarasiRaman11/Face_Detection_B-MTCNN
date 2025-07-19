# Face Detection Web App

This web application allows users to upload an image and detect faces using two different algorithms: MTCNN and B-MTCNN.

## Features
- Upload an image and detect faces
- Two face detection methods: MTCNN and B-MTCNN
- Results displayed with bounding boxes around detected faces

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Flask application:
   ```bash
   python app.py
   ```

## Usage
- Open `http://127.0.0.1:5000/` in your browser.
- Upload an image.
- Click `MTCNN` or `B-MTCNN` to detect faces.

## Requirements
- Python 3.x
- Flask
- OpenCV
- NumPy
- MTCNN

