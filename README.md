# Deep-Vision-Voyager

**Microcontroller:** Raspberry Pi 4
**Other hardware:** Motor, l298n motor driver, webcam, Wi-Fi adapter, SG90 servo motor, power bank
**Deep learning architecture for object detection:** YOLO v3 

This is our CSE 316 project named “DeepVision Voyager” which is basically a moving robot controlled by a computer located remotely using socket programming over wifi network. It captures live video from its surroundings and streams it in server computer and finally it can detect objects with high precision from its live video stream. Its camera angle can also be adjusted by servo motor. The central processing unit has Raspberry Pi 4 in it.
The object detection part is inevitably done by deep learning. We used YOLOv3 architecture. Our architecture of YOLO v3 is based on a deep convolutional neural network (CNN) which is designed to detect and localize objects within an image in a single forward pass.
YOLO v3 uses a variant of Darknet, which originally has 53 layer network trained on Imagenet. For the task of detection, 53 more layers are stacked onto it, giving us a 106 layer fully convolutional underlying architecture. In YOLO v3, the detection is done by applying 1x1 detection kernels on feature maps of three different sizes at three different places in the network. It uses binary cross-entropy for calculating the classification loss for each label while object confidence and class predictions are predicted through logistic regression. 

