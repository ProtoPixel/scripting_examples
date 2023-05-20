from __future__ import division
from builtins import object
from past.utils import old_div
from protopixel import Content
from openframeworks import *

X = 0.0
Y = 0.0

mode = "rest"

content = Content("Orientation Script")
content.web_path("orientation")

content.FBO_SIZE = (500, 500)


class Autoscale(object):
    def __init__(self, min_value, max_value):
        self.min_out = min_value
        self.max_out = max_value
        self.spread_out = self.max_out - self.min_out
        self.min = self.max = None

    def __call__(self, val):
        if self.min is None:
            self.min = self.max = val
            return self.min_out + (self.spread_out) / 2.0

        self.min = min(self.min, val)
        self.max = max(self.max, val)

        return self.min_out + self.spread_out * (
            old_div((val - self.min), (self.max - self.min))
        )


autoscalex = Autoscale(0.0, 1.0)
autoscaley = Autoscale(0.0, 1.0)


def draw():
    global X, Y
    ofClear(0)
    colorV = ofColor(255, 50, 0) * X + ofColor(50, 255, 0) * (1 - X)
    colorH = ofColor(255, 50, 0) * Y + ofColor(50, 255, 0) * (1 - Y)
    ofSetColor(colorV)
    if mode == "rest":
        w = content.FBO_SIZE[0] / 8.0
        h = content.FBO_SIZE[1] / 8.0
        ofDrawEllipse(
            X * content.FBO_SIZE[0], content.FBO_SIZE[1] / 2.0, w, content.FBO_SIZE[1]
        )
        ofSetColor(colorH)
        ofDrawEllipse(
            content.FBO_SIZE[0] / 2.0,
            Y * content.FBO_SIZE[1],
            0,
            content.FBO_SIZE[0],
            h,
        )
    else:
        ofDrawRectangle(0, 0, *content.FBO_SIZE)


@content.websocket.receive
def ws_handle(ws, data):
    set_x(-data["z"])
    set_y(data["y"])


def set_x(x):
    global X
    x = autoscalex(x)
    X = X * 0.9 + x * 0.1


def set_y(y):
    global Y
    y = autoscaley(y)
    Y = Y * 0.9 + y * 0.1
