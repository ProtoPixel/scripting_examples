# Player remote interface

from protopixel import Content

# We neeed access to low level API calls for communication with core
from protopixel.core import callParameterProgram

# Define content
content = Content('Player Remote Interface Script')
content.add_parameter('video_content', value='video')

# Place where we have the custom remote interface
content.web_path('player_remote_interface')


# manage websocket incoming messages
@content.websocket.receive
def websocket(ws, data):
    # the message is a JSON like {"action":"play"}
    action = data.get('action')
    if action == 'play':
        # Play video
        # callParameterProgram is used to "push a button" of a particular content
        # In this case, the button for play/pause has the name 'pause/resume' and it
        # is in the section 'params', so the full name is 'params:pause/resume'.
        callParameterProgram(parameters.video_content, 'params:pause/resume')
    elif action == 'pause':
        # Pause video
        callParameterProgram(parameters.video_content, 'params:pause/resume')

    # In the case that we want to modify a parameter of another content, instead of just pushing a button
    # We should use saveConfProgram from the module protopixel.core. For instance:
    # saveConfProgram(parameters.video_content,'params:position','0.0')
    # would place the video position to 0.0.
