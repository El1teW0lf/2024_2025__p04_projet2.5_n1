from ursina import *

psx_frag = ""
with open("shaders/psx_frag.glsl","r") as file:
    psx_frag = file.read()

psx_vert = ""
with open("shaders/psx_vert.glsl","r") as file:
    psx_vert = file.read()



psx_shader = Shader(name='unlit_shader', language=Shader.GLSL, vertex =  psx_vert, fragment= psx_frag)
