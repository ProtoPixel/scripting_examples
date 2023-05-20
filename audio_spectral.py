from __future__ import division
from past.utils import old_div
from openframeworks import *
from protopixel import Content
import numpy as np

window = 255

content = Content("Audio Script")
content.FBO_SIZE = window
content.add_parameter("low_limit", value=10, min=0, max=window)
content.add_parameter("high_limit", value=83, min=0, max=window)
content.add_parameter("trail", value=0.3, min=0.0, max=1.0)

scale_limit = 0.001

max_low = scale_limit
max_mid = scale_limit
max_high = scale_limit

last_low = 0.0
last_mid = 0.0
last_high = 0.0


def draw():
    """
    To get the spectrum of the audio you can use the fft buffer:
    >>> content.get_fft_buffer() #get spectral buffer as a numpy array
    """
    global max_low, max_mid, max_high, last_high, last_mid, last_low
    # we use the energy to change the color
    ofClear(0, 0, 0, 255)

    b = content.get_fft_buffer()

    low_limit = content["low_limit"]
    high_limit = content["high_limit"]

    low = np.sqrt(np.mean(b[:low_limit] ** 2))
    mid = np.sqrt(np.mean(b[low_limit:high_limit] ** 2))
    high = np.sqrt(np.mean(b[high_limit:] ** 2))

    max_low = max(max_low, low)
    max_mid = max(max_mid, mid)
    max_high = max(max_high, high)

    low = old_div(low, max_low) * window
    mid = old_div(mid, max_mid) * window
    high = old_div(high, max_high) * window

    trail = content["trail"]
    low = max(low * trail + last_low * (1.0 - trail), low)
    mid = max(mid * trail + last_mid * (1.0 - trail), mid)
    high = max(high * trail + last_high * (1.0 - trail), high)
    last_low = low
    last_mid = mid
    last_high = high

    ofSetColor(255, 0, 0, 255)
    ofDrawRectangle(0, 0, old_div(window, 3), int(low))
    ofSetColor(0, 255, 0, 255)
    ofDrawRectangle(old_div(window, 3), 0, old_div(window, 3), int(mid))
    ofSetColor(0, 0, 255, 255)
    ofDrawRectangle(old_div(window, 3) * 2, 0, old_div(window, 3), int(high))


@content.add_button("reset_scale")
def reset_scale():
    global max_low, max_mid, max_high
    max_low = scale_limit
    max_mid = scale_limit
    max_high = scale_limit
