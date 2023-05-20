from openframeworks import *
from protopixel import Content

size = 255

# color is the current color displayed,
# color2 is the last color received
color = ofColor(255, 255, 255)
color2 = ofColor(255, 255, 255)

content = Content("Custom Art-Net Script")
content.FBO_SIZE = (size, size)


def update():
    """
    As we receive these messages at a lower rate than the framerate, we use a running
    average to interpolate between values.
    """
    global color
    color = color * 0.9 + color2 * 0.1


def draw():
    """
    We use r,g,b to draw the three bars.
    """
    ofClear(0)
    ofSetColor(color)
    ofDrawRectangle(0, 0, size / 3.0, color.r)
    ofDrawRectangle(size / 3.0, 0, size / 3.0, color.g)
    ofDrawRectangle(2.0 * size / 3.0, 0, size / 3.0, color.b)


# We listen for ArtNet Values. To do so we use the content.artnet decorator.
# The first argument is the DMX channel, the second one (and optional) is the universe
# The decorated function receives the value of the channel


@content.artnet(1, universe=0)
def r1(v):
    color2.r = v


@content.artnet(2)
def r1(v):
    color2.g = v


@content.artnet(3)
def r1(v):
    color2.b = v
