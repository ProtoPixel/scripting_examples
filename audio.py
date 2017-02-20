from openframeworks import *
from protopixel import Content
import numpy as np

content = Content("Audio Script")

def draw():
    """
    To pocess audio input, we can use the audio input buffer.
    >>> content.get_sound_buffer() #get audio buffer as a numpy array
    """
    buffer = content.get_sound_buffer()

    # get the absolute values 
    buffer = np.abs(buffer)

    # get the sum of all values, to measure the energy
    energy = int(buffer.sum())

    # we use the energy to change the color
    ofClear(min(255,energy),0,0,255)

