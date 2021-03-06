from protopixel import Content
from openframeworks import *

import os.path
from tempfile import mkdtemp

content = Content("Shader")
content.add_parameter("shader path", type="filepath")
content.add_parameter("speed", value=1.0, min=0.0, max=10.0)
content.add_parameter("reset 24h", value=False)

side = 256
content.FBO_SIZE = (side,side)
shader = ofShader()

temp_dir = mkdtemp()
frag_file = os.path.join(temp_dir,'s.frag')
vert_file = os.path.join(temp_dir,'s.vert')
shader_file_of = os.path.join(temp_dir,'s')

def setup():
    if content['shader path']:
        shader_path_changed(content['shader path'])

def draw():
    ofClear(0,0,0,255)
    if shader.isLoaded():
        if content['reset 24h']:
            time = ofGetElapsedTimeMillis() % 86400000
            time = time / 1000.0
        else:
            time = ofGetElapsedTimef()
        shader.begin()
        shader.setUniform3f('iResolution', float(content.FBO_SIZE[0]), float(content.FBO_SIZE[1]),0.0)
        shader.setUniform1f('iGlobalTime', time*content['speed'])
        ofDrawRectangle(-side/2.,-side/2.,side,side)
        shader.end()

@content.parameter_changed('shader path')
def shader_path_changed(p):
    frag_contents = open(p).read()
    with open(frag_file,'w') as f:
        f.write(frag_contents_prefix)
        f.write(frag_contents)
        f.write(frag_contents_suffix)
    with open(vert_file,'w') as f:
        f.write(vert_contents)
    shader.load(shader_file_of)

def on_enable():
    if content['shader path']:
        shader_path_changed(content['shader path'])

vert_contents = """
#version 150

in vec4 position;
out vec4 position_frag;

void main() {
	gl_Position = position;
	position_frag = position;
}
"""

frag_contents_prefix = """
#version 150
out vec4 outputColor;
uniform vec3 iResolution;
uniform float iGlobalTime;

in vec4 position_frag;
"""

frag_contents_suffix = """
void main()
{
    vec2 pos = position_frag.xy;
    pos.x /= 2.0;
    pos.y /= -2.0;
    pos.x += 0.5;
    pos.y += 0.5;
    pos.x *= iResolution.x;
    pos.y *= iResolution.y;
    mainImage( outputColor, pos);
}
"""
