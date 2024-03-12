import socket
import time
from gpiozero import Motor
from gpiozero import LED
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
factory = PiGPIOFactory()
servo = Servo(3, min_pulse_width=0.5/1000,
              max_pulse_width=2.5/1000, pin_factory=factory)
frlight = LED(6)
fllight = LED(12)
bllight = LED(21)
brlight = LED(13)
frmotor = Motor(forward=22, backward=23)
flmotor = Motor(forward=9, backward=25)
blmotor = Motor(forward=4, backward=14)
brmotor = Motor(forward=17, backward=18)
speed = 0.25


def lightStop():
    frlight.off()
    fllight.off()
    bllight.off()
    brlight.off()


def left():
    global speed
    flmotor.backward(speed)
    frmotor.forward(speed)
    blmotor.backward(speed)
    brmotor.forward(speed)
    fllight.on()
    bllight.on()


def right():
    global speed
    flmotor.forward(speed)
    frmotor.backward(speed)
    blmotor.forward(speed)
    brmotor.backward(speed)
    frlight.on()
    brlight.on()


def forward():
    global speed
    flmotor.forward(speed)
    frmotor.forward(speed)
    blmotor.forward(speed)
    brmotor.forward(speed)
    frlight.on()
    fllight.on()


def reverse():
    global speed
    flmotor.backward(speed)
    frmotor.backward(speed)
    blmotor.backward(speed)
    brmotor.backward(speed)
    brlight.on()
    bllight.on()


def stop():
    flmotor.stop()
    frmotor.stop()
    blmotor.stop()
    brmotor.stop()
    lightStop()


CAM = 0.07
servo.value = 0.0
velCam = 0.0
isStop = True


def camLeft():
    global isStop, velCam, CAM
    isStop = False
    velCam = CAM


def camRight():
    global isStop, velCam, CAM
    isStop = False
    velCam = -CAM


def camStop():
    global isStop, velCam, CAM
    isStop = True
    velCam = 0


s = socket.socket()
host = '172.20.10.4'
port = 12760
while True:
    try:
        s.connect((host, port))
        break
    except:
        print("Failed, trying again")
        time.sleep(2)
        continue
while True:
    try:
        pp = s.recv(1024)
        data = pp.decode()
    except socket.timeout:
        data = ''
    print(data)
    if data == 'forward':
        forward()
    if data == 'reverse':
        reverse()
    if data == 'left':
        left()
    if data == 'right':
        right()
    if data == 'camlef':
        camLeft()
    if data == 'camrig':
        camRight()
    if data == 'stop':
        stop()
        camStop()
    if data == 'sup':
        if speed < 1:
            speed += 0.05
    if data == 'sdown':
        if speed > 0:
            speed -= 0.05
    if isStop:
        camStop()
        if velCam != 0:
            servo.value += velCam
    else:
        if velCam > 0 and servo.value < 0.92:
            servo.value += velCam
        elif velCam < 0 and servo.value > -0.92:
            servo.value += velCam

s.close()
