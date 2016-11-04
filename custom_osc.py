from openframeworks import *
from protopixel import Content

size = 255

# color is the current color displayed,
# color2 is the last color received
color = ofColor(255, 255, 255)
color2 = ofColor(255, 255, 255)

content = Content('Custom OSC Script')
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


def normalize(c):
    """
    Map the values from the accelerometer to 0-255
    """
    c = c / 20.0 + .5
    c *= 255
    return max(0, min(255, c))


@content.OSC('/acc')
def acceleration(x, y, z):
    """
    This function handles OSC user input in address "/acc", with 3 arguments: x,y,z.
    Use pl.OSC decorator to define handles like this. Multiple scripts can listen to
    the same address simultaneously.
    """
    global color2
    r = normalize(x)
    g = normalize(y)
    b = normalize(z)
    color2 = ofColor(r, g, b)
