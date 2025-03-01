#version 330 core

layout(location = 0) in vec4 in_position;   
layout(location = 1) in vec2 in_texcoord;   
layout(location = 2) in float in_depth;      
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;

uniform float Jitter;
uniform mat4 p3d_ModelViewProjectionMatrix;

out vec2 v_texcoord;  
out float v_depth;    

void main() {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    //gl_Position = round(gl_Position /Jitter ) * Jitter;
    v_texcoord = p3d_MultiTexCoord0; 
    v_depth = gl_Position.w;
}
