# This file is part of the ProtoPixel Library
from protopixel import Content
from openframeworks import *
from collections import namedtuple

content = Content('Paint')
content.add_parameter('size', value=300, min=0, max=1024)
content.add_parameter('cleat', type='button')

firstrun = True
Finger = namedtuple('Finger', ['x', 'y', 'size', 'color'])
fingers = []

content.FBO_SIZE = (300, 300)
content.web_path('paint')


@content.parameter_changed('size')
def size_changed(size):
    content.FBO_SIZE = (size, size)


@content.websocket.receive
def websocket(ws, data):
    if data['event'] == "draw":
        getfinger(
            data['x'] * content.FBO_SIZE[0],
            data['y'] * content.FBO_SIZE[1],
            data['color'])
    elif data['event'] == "clear":
        clear()


def getfinger(x, y, color):
    fingers.append(Finger(x, y, 10, color))


@content.add_button('clear')
def clear():
    global firstrun
    firstrun = True


def draw():
    global firstrun, fingers
    if firstrun:
        firstrun = False
        ofClear(0, 0, 0, 0)

    ofPushMatrix()
    for finger in fingers:
        ofSetColor(*finger.color)
        ofCircle(finger.x, finger.y, finger.size)
    ofPopMatrix()

    fingers = []


def on_enable():
    clear()
