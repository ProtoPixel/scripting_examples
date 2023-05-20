# Activating/deactivating contents by OSC or button

# In this scenario we have two contents that we want to control, their names are "content1" and "content2"

from protopixel import Content

# We need to change the configuration of other contents
from protopixel.core import setConfContent

# Create ProtoPixel Create content
content = Content("OSC and button Content enabler example")

# content.add_button decorator adds a button on the GUI that executes the decorated function
# content.OSC decorator let's you define an OSC entry point for a given address. In this case
# '/scene1' address with no arguments will execute this function
@content.add_button("scene1")
@content.OSC("/scene1")
def enable_scene1():
    # When we receive an OSC packet in '/scene1' or click on 'scene1' button, we activate content1
    # and deactivate content2
    setConfContent("content1", "enabled", True)
    setConfContent("content2", "enabled", False)


@content.add_button("scene2")
@content.OSC("/scene2")
def enable_scene2():
    # When we receive an OSC packet in '/scene2' or click on 'scene2' button, we activate content2
    # and deactivate content1
    setConfContent("content1", "enabled", False)
    setConfContent("content2", "enabled", True)
