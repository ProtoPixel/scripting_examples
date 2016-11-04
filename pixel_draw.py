from openframeworks import *
import numpy as np
from protopixel import Content

# You can paint directly your light points by using numpy arrays

content = Content('Pixel Draw Script')
content.FBO_SIZE = (170, 170)

# we can precalculate this
center = np.array(content.FBO_SIZE) / 2


def draw_pixels(position_array, colors_array):
    """
    This function is called at every frame, with two arguments:
    * position_array is an array of 2D positions of all our lights
    * colors_array is an array of RGBA color components that we have
        to fill in order to "paint" our leds

    Please note that we have to CHANGE the contents of colors_array,
    not to assign a new array to the variable:

    >>> colors_array[:] = computed_colors # Correct
    >>> colors_array = computed_colors # Incorrect
    """
    t = ofGetElapsedTimef()
    dx = position_array[:, 0] - center[0]  # position_array[:,0] is all x positions
    dy = position_array[:, 1] - center[1]  # position_array[:,1] is all y positions
    dist = np.sqrt(dx * dx + dy * dy)
    r = np.sin(dist / 10 - t * 5) * .5 + .5
    colors_array[:, 0] = r  # Red
    colors_array[:, 1] = 0.0  # Green
    colors_array[:, 2] = 1.0 - r  # Blue
    colors_array[:, 3] = 1.0  # Opacity
