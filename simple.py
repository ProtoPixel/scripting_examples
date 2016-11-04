from openframeworks import *
from protopixel import Content
from random import randint

print "Hello ProtoPixel"

content = Content("Simple Script")
content.FBO_SIZE = (170,170) #optional: define size of FBO, default=(100,100)

#a global variable
counter = 0


# None of the following functions are mandatory, they can be omitted


def setup():
    """
    This will be called at the beggining, you set your stuff here
    """
    pass


def update():
    """
    For every frame, before drawing, we update stuff
    """
    global counter
    counter = counter + 0.033


def draw():
    """
    For every frame draw stuff. Do not forget to clear the frmebuffer!
    """
    ofClear(0,0,0)
    ofFill()
    for i in range(0,200):
        ofSetColor(randint(0, 255), randint(0, 255), randint(0, 255))
        ofRect(randint(0, 150), randint(0, 150),
                randint(10, 20), randint(10, 20))


def exit():
    """
    Before removing the script, in case you have pending business.
    """
    pass


def on_enable():
    """
    This function is called when this content just got enabled.
    """
    pass


def on_disable():
    """
    This function is called when this content just got disabled.
    `update` and `draw` functions are not called while this content is disabled.
    """
    pass
