#version 330

uniform sampler2D p3d_Texture0; // Texture sampler
uniform vec3 FogColor;
uniform float FogDensity;
uniform float PixelScale;
uniform float ColorDepth;

in vec2 v_texcoord;
in float v_depth;

out vec4 fragColor;

void main() {
    vec4 col = texture(p3d_Texture0, v_texcoord);
    vec4 col2 = col / (4.0 / col);

    vec2 cord = gl_FragCoord.xy / PixelScale;
    float cbrd = mod(floor(cord.x) + floor(cord.y), 2.0);
    col += col2 * cbrd;

    col = round(col * ColorDepth) / ColorDepth ;

    float fogFactor = 1.0 - exp(-FogDensity * v_depth);
    vec3 foggedColor = mix(col.rgb, FogColor, fogFactor);

    fragColor = vec4(foggedColor, col.a);
}
