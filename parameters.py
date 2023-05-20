from __future__ import print_function
from builtins import str
from builtins import range
from openframeworks import *
from protopixel import Content

content = Content("Parameters Script")

# You can define parameters that will show in the GUI
# The supported parameter types are:
# boolean
#   True or False
# integer
# float
#   Can define a min and max
# string
#   A simple string
# filepath
#   A string, but a button for opening a file will appear
# color
#   An instance of ofColor (r,g,b,a).
# button
#   A function that can be triggered
# choice
#   A string, but with limited options


# Use content.add_parameter to define all parameters of the script that will be exposed to the GUI
# The first argument is the name of the variable,
# the keywords are the options.
# Booleans do not have options other that its initial value.
# Initial value is optional.
# Pay attention to the type of the value. If you mix them you will
# get incorrect types (1 vs 1.0 for int and float, for instace)
content.add_parameter("a_boolean", value=True)

# Integer can also define min and max of its value.
content.add_parameter("a_integer", min=0, max=5, value=5)

# Float works the same way as int.
# For both, `min` and `max` are optional.
content.add_parameter("a_float", min=0.0, max=5.0, value=0.0)

# Strings do not have options.
content.add_parameter("a_string", value="Hello")

# For filepaths you have to specify its type.
# type can also be specified for the previous types, they are otherwise inferred.
content.add_parameter("a_filepath", type="filepath")

# The same goes for color
# The default value for color is RGBA(0,0,0,0)
content.add_parameter("a_color", type="color", value=ofColor(0, 0, 0))

# Experimental Tunable White Color (warm, intensity)
# The default value for tunablewhitw is (0,0)
content.add_parameter("a_tunablewhite", type="tunablewhite", value=(0, 0))


@content.parameter_changed("a_tunablewhite")
def whites_changed(newval):
    print("New Tunable White Color:", newval)


# Buttons as well.
# If you don't specify the buttons here they will be automatically added at the end.
content.add_parameter("a_button", type="button")

# Choices are strings, but with a limited set of options for the user to choose from
# use `options` keyword to define the possible values.
content.add_parameter(
    "a_choice", type="choice", value="A", options=["A", "B", "C", "D"]
)

# `options`can also be a function returning the list of options. This is very useful to
# generate the options in real time.
def gen_options():
    print("Generating options!")
    return [str(n) for n in range(10)]


content.add_parameter("a_choice_f", type="choice", value="1", options=gen_options)


# By using the "display_name" parameter, you can add better names to your parameters
content.add_parameter(
    "ugly_param_name", value=True, display_name="Nice Readable Parameter"
)

# If you want to hide this parameter from the user, use the "hidden" option
content.add_parameter("secret_data", value="mypassword", hidden=True)


@content.parameter_changed("a_filepath")
def filepath_changed(newval):
    print("New path:", newval)


# We must manually add buttons. You can use content.add_button to link the
# button to the function


@content.add_button("a_button")
def a_button():
    """
    Buttons are just global functions. No parameters
    """
    print("You clicked a_button!")


# We can subscribe to changes on any parameter
# every time the user changes a parameter in the GUI we will receive a notification
# To do so use content.parameter_changed(parameter_name)


@content.parameter_changed("a_integer")
def parameter_changed(value):
    """
    This function is called every time a a_integer is changed.
    We get the new value as an argument
    """
    print("You changed parameter a_integer")
    # we can also modify those parameters and the controls
    # on the gui will also get modified
    content["a_float"] = float(value)


@content.parameter_changed("a_choice")
def choice_changed(newval):
    print("New choice value:", newval)


def draw():
    ofClear(0)
    # You can access a parameter throug `parameters` variable
    ofSetColor(content["a_color"])
    # We can modify the resolution of the content canvas by modifying content.FBO_SIZE
    # By default content.FBO_SIZE = (128,128)
    ofDrawRectangle(
        0, 0, content.FBO_SIZE[0] * content["a_float"] / 5.0, content.FBO_SIZE[1]
    )
