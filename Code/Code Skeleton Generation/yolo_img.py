import cv2
import numpy as np
import sys

def yolo_ret():
    # Load Yolo
    net = cv2.dnn.readNet("D:/Projects/O-SE-R/Code/YOLO model/yolov3_custom_final.weights", "D:/Projects/O-SE-R/Code/YOLO model/yolov3_custom.cfg")
    classes = []
    with open("D:/Projects/O-SE-R/Dataset/images/classes.txt", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    if sys.version_info >= (3, 9):
        output_layers = [layer_names[i- 1] for i in net.getUnconnectedOutLayers()]
    else:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    # Loading image
    img = cv2.imread("D:/Projects/O-SE-R/Dataset/images/70.jpg")
    #img = cv2.resize(img, (1280,720))
    #img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
    #        if confidence >= 0.1:
            # Object detected
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            print(detection[3] * height)
            h = int(detection[3] * height)

            # Rectangle coordinates
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.5)
    font = cv2.FONT_HERSHEY_PLAIN
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, img = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY_INV)

    return (img,boxes,indexes,class_ids)