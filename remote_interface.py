from __future__ import print_function
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
content.web_path("remote_interface")


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
    r = data["r"]
    g = data["g"]
    b = data["b"]
    color = ofColor(r, g, b)

    """
    Once we have received the colors we can send them back through the websocket
    """
    ws.send(data)


def draw():
    """
    Draw a simple rectangle that displays the color.
    """
    ofClear(0)
    ofSetColor(color)
    ofDrawRectangle(0, 0, size, size)


# You can also process the events of connection and disconnection for websockets:


@content.websocket.new
def websocket_new(ws):
    print("New websocket connection!")


@content.websocket.close
def websocket_close(ws):
    print("Websocket connection closed!")
