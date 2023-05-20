# This file is part of the ProtoPixel Library
from builtins import range
from protopixel import Content
from openframeworks import *
from collections import namedtuple
import json

content = Content("Paint")
content.add_parameter("size", value=300, min=0, max=1024)
content.add_parameter("clear", type="button")
content.add_parameter("canvas_content", value="[]")

firstrun = True
Finger = namedtuple("Finger", ["x", "y", "x2", "y2", "size", "color"])
fingers = []
fingers_hist = []
fingers_hist_dirty = False

content.FBO_SIZE = (300, 300)
content.web_path("paint")


@content.parameter_changed("size")
def size_changed(size):
    content.FBO_SIZE = (size, size)


@content.parameter_changed("canvas_content")
def draw_canvas_content(c):
    global fingers_hist, fingers_hist_dirty, fingers
    cc = [Finger(*t) for t in json.loads(c)]
    fingers_hist = cc
    fingers = cc
    fingers_hist_dirty = True


@content.websocket.new
def new_websocket(ws):
    sendfingers = [list(f) for f in fingers_hist]
    for f in sendfingers:
        f[0] /= content.FBO_SIZE[0]
        f[1] /= content.FBO_SIZE[1]
        f[2] /= content.FBO_SIZE[0]
        f[3] /= content.FBO_SIZE[1]
    ws.send({"lines": sendfingers})


@content.websocket.receive
def websocket(ws, data):
    event = data.get("event")
    if event == "draw":
        getfinger(
            data["x"] * content.FBO_SIZE[0],
            data["y"] * content.FBO_SIZE[1],
            data["x2"] * content.FBO_SIZE[0],
            data["y2"] * content.FBO_SIZE[1],
            data["color"],
        )
    elif event == "clear":
        clear()


def getfinger(x, y, x2, y2, color):
    global fingers_hist_dirty
    f = Finger(x, y, x2, y2, 10, color)
    fingers.append(f)
    fingers_hist.append(f)
    fingers_hist_dirty = True


@content.add_button("clear")
def clear():
    global firstrun, fingers_hist_dirty
    firstrun = True
    fingers_hist[:] = []
    fingers_hist_dirty = True


def setup():
    draw_canvas_content(content["canvas_content"])


def update():
    global fingers_hist_dirty
    if fingers_hist_dirty:
        fingers_hist_dirty = False
        content["canvas_content"] = json.dumps([tuple(f) for f in fingers_hist])


def draw():
    global firstrun, fingers
    if firstrun:
        firstrun = False
        ofClear(0, 0, 0, 0)

    ofPushMatrix()
    for finger in fingers:
        ofSetColor(*finger.color)

        diff_x = int(finger.x2 - finger.x)
        sx = 1 if diff_x > 0 else -1
        diff_y = int(finger.y2 - finger.y)
        sy = 1 if diff_y > 0 else -1
        ofDrawCircle(finger.x2, finger.y2, finger.size)
        for n in range(int(sx * diff_x)):
            n = n * sx
            x = finger.x + n
            y = finger.y + float(n) / diff_x * diff_y
            ofDrawCircle(x, y, finger.size)
        for n in range(int(sy * diff_y)):
            n = n * sy
            x = finger.x + float(n) / diff_y * diff_x
            y = finger.y + n
            ofDrawCircle(x, y, finger.size)

    ofPopMatrix()
    fingers = []
