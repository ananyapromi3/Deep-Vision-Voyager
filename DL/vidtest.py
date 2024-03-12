import cv2
import numpy as np
import pyttsx3
engine = pyttsx3.init()
net = cv2.dnn.readNet(r"/Users/ananyashahrinpromi/Documents/BUET/project_316_DL/yolov3.weights",
                      r"/Users/ananyashahrinpromi/Documents/BUET/project_316_DL/yolov3.cfg.txt")
classes = []
with open(r"/Users/ananyashahrinpromi/Documents/BUET/project_316_DL/coco.names.txt", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1]
                 for i in net.getUnconnectedOutLayers().flatten()]
url = "http://172.20.10.5:8081/stream_simple.html"
cap = cv2.VideoCapture(url)
while True:
    ret, img = cap.read()
    if not ret:
        break
    height, width, channels = img.shape
    width = 1000
    height = 720
    img = cv2.resize(img, (width, height))
    # Detecting objects
    blob = cv2.dnn.blobFromImage(
        img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, f"{label} {int(confidence * 100)}%",
                        (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            if label == 'bottle':
                print(
                    f"Detected target with confidence {confidence * 100:.2f}%")
                engine.say("Bottle Detected ")
                engine.runAndWait()
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:  # ESC key to break
        break
cap.release()
cv2.destroyAllWindows()
