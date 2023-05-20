from openframeworks import *
from protopixel import Content
import numpy as np

content = Content("Assets example Script")


# If you want to use an external asset inside a script
# you can declare it like this:

cat_file = content.add_asset("cat.jpeg")

# This could be a file or a folder.

# This serves two different purposes:
# - It is equivalent to os.path.join(os.path.dirname(__file__),'cat.jpeg'),
#   so it allows you to get a valid path for an asset that is relative to
#   the script, but is easier to write.
# - It tells ProtoPixel Create about these files, so it can pack them when
#   exporting a project.


def setup():
    global image
    image = ofImage(cat_file)
    content.FBO_SIZE = (int(image.getWidth()), int(image.getHeight()))


def draw():
    image.draw(0, 0)
