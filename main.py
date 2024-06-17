from flask import Flask, send_file
import cv2
import threading
import time

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def capture_frames():
    global camera
    while True:
        time.sleep(0.2)
        success, frame = camera.read()
        if not success:
            break
        cv2.imwrite('current_frame.jpg', frame)

thread = threading.Thread(target=capture_frames)
thread.daemon = True
thread.start()
@app.route('/face')
def face():
    frame = cv2.imread('current_frame.jpg')
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
    cv2.imwrite('current_frame.jpg', frame)
    return send_file('current_frame.jpg', mimetype='image/jpg')


while True:
    imagePath = 'current_frame.jpg'
    img = cv2.imread(imagePath)
    
    if img is None:
        print("Erreur : l'image n'a pas pu être chargée.")
        break
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    face = face_classifier.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
    )
    for (x, y, w, h) in face:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imwrite('rendue.jpg', img)
    time.sleep(0.2)
if __name__ == "__main__":
    app.run(debug=True)