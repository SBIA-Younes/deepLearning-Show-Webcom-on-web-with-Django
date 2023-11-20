from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time




from django.contrib.auth.views import LoginView
from .models import BlogPost


class AccountLoginView(LoginView):
    template_name = 'login.html'


def home(request):
    if not request.user.is_authenticated:
        blog_post = BlogPost.objects.filter(published=True, internet=True).order_by('-created_on')[:6]
    else:
        blog_post = BlogPost.objects.filter(published=True).order_by('-created_on')[:6]

    context = {
      "posts" : blog_post
    }
    return render(request, "base.html", context)



# Load model file
net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")

# ModelNet SSD Object list init
CLASSES = ["arriere-plan", "avion", "velo", "oiseau", "bateau",
           "bouteille", "autobus", "voiture", "chat", "chaise", "vache", "table",
           "chien", "cheval", "moto", "personne", "plante en pot", "mouton",
           "sofa", "train", "moniteur"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# Function to perform object detection on a frame

def perform_object_detection(frame):
    # Create blob from image
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

    # Feed input to neural network
    net.setInput(blob)
    detections = net.forward()

    # Detection loop
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.2:  # Adjust confidence threshold as needed
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            
            cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

    return frame



def stream():
    vs = VideoStream(src=0, resolution=(1600, 1200)).start()
    time.sleep(2.0)
    fps = FPS().start()

    while True:
      frame = vs.read()

      if frame is None:
          print('Error: failed to capture image')
          continue

      frame = imutils.resize(frame, width=800)
      frame_with_detections = perform_object_detection(frame)

      image_bytes = cv2.imencode('.jpg', frame_with_detections)[1].tobytes()
      yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')
    


def video_feed(request):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')



def streamPage(request):
  return render(request, "stream.html",)