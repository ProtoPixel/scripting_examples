from protopixel import Content
from openframeworks import *

import os.path
from tempfile import mkdtemp

content = Content("Shader")
content.add_parameter("shader path", type="filepath")
content.add_parameter("speed", value=1.0, min=0.0, max=10.0)
content.add_parameter("reset 24h", value=False)

side = 256
content.FBO_SIZE = (side, side)
shader = ofShader()

temp_dir = mkdtemp()
frag_file = os.path.join(temp_dir, "s.frag")
vert_file = os.path.join(temp_dir, "s.vert")
shader_file_of = os.path.join(temp_dir, "s")


def reset_vars():
    global iTime, iFrame
    iTime = 0
    iFrame = 0


def setup():
    reset_vars()
    if content["shader path"]:
        shader_path_changed(content["shader path"])


one_day_in_seconds = 60 * 60 * 24


def draw():
    global iTime, iFrame
    ofClear(0, 0, 0, 255)
    if shader.isLoaded():
        if content["reset 24h"] and iTime > one_day_in_seconds:
            iTime = iTime - one_day_in_seconds
        timedelta = ofGetLastFrameTime() * content["speed"]
        iTime += timedelta
        iFrame += 1
        iMouse = (ofGetMouseX(), ofGetMouseY())
        shader.begin()
        shader.setUniform3f(
            "iResolution", float(content.FBO_SIZE[0]), float(content.FBO_SIZE[1]), 0.0
        )
        shader.setUniform1f("iGlobalTime", iTime)
        shader.setUniform1f("iTime", iTime)
        shader.setUniform1f("iFrame", iFrame)
        shader.setUniform4f("iMouse", 0.0, 0.0, 0.0, 0.0)
        shader.setUniform1f("iTimeDelta", timedelta)
        shader.setUniform4f("iChannelTime", 0.0, 0.0, 0.0, 0.0)
        ofDrawRectangle(-side / 2.0, -side / 2.0, side, side)
        shader.end()


@content.parameter_changed("shader path")
def shader_path_changed(p):
    reset_vars()
    if not p:
        return
    frag_contents = open(p).read()
    with open(frag_file, "w") as f:
        f.write(frag_contents_prefix)
        f.write(frag_contents)
        f.write(frag_contents_suffix)
    with open(vert_file, "w") as f:
        f.write(vert_contents)
    shader.load(shader_file_of)


def on_enable():
    if content["shader path"]:
        shader_path_changed(content["shader path"])


@content.add_button("reload shader")
def reload_file():
    shader_path_changed(content["shader path"])


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
uniform float iGlobalTime; // legacy?

uniform vec3      iResolution;           // viewport resolution (in pixels)
uniform float     iTime;                 // shader playback time (in seconds)
uniform float     iTimeDelta;            // render time (in seconds)
uniform int       iFrame;                // shader playback frame
uniform vec4      iMouse;                // mouse pixel coords. xy: current (if MLB down), zw: click

in vec4 position_frag;

//Not implemented but tolerated

/*uniform*/ vec4      iDate;                 // (year, month, day, time in seconds)
/*uniform*/ float     iSampleRate;           // sound sample rate (i.e., 44100)

//Not implemented

/*
uniform float     iChannelTime[4];       // channel playback time (in seconds)
uniform vec3      iChannelResolution[4]; // channel resolution (in pixels)
uniform samplerXX iChannel0..3;          // input channel. XX = 2D/Cube
*/

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
