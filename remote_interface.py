from openframeworks import *
from protopixel import Content

# color is the current color displayed
color = ofColor(255, 255, 255)

content = Content("Remote Interface Script")
size = 255

content.FBO_SIZE = (size, size)

# Here we specify where the remote interface (HTML) is.
# In this case, we have the index.html file in a folder
# called "remote_interface"
content.web_path('remote_interface')


@content.websocket.receive
def websocket(ws, data):
    """
    This function handles user input through a websocket, as provided in /pl.js library.
    Use content.websocket.receive decorator to define handles like this.
    In this case we send the accelerometer readings of the device (x,y,z).
    `ws` is a websocket, data the data comming through the websocket. You can send data
    with `ws.send()`.
    """
    global color
    r = normalize(data["x"])
    g = normalize(data["y"])
    b = normalize(data["z"])
    color = ofColor(r, g, b)


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
    if c is None:
        return 0
    c = c / 20.0 + .5
    c *= 255
    return max(0, min(255, c))


# You can also process the events of connection and disconnection for websockets:

@content.websocket.new
def websocket_new(ws):
    print "New websocket connection!"


@content.websocket.close
def websocket_close(ws):
    print "Websocket connection closed!"
