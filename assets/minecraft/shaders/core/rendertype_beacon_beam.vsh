#version 150

in vec3 Position;
in vec4 Color;
in vec2 UV0;

uniform sampler2D Sampler0;

uniform mat4 ModelViewMat;
uniform mat4 ProjMat;

out vec4 vertexColor;
out vec2 texCoord0;

void main() {
    vertexColor = Color;
    texCoord0 = UV0;

    vec4 c = texture(Sampler0, texCoord0);
    if (c.rgb == vec3(0.0, 0.0, 0.0)) {
        gl_Position = ProjMat * ModelViewMat * vec4(vec3(0.0,0.0,0.0), 1.0);
    } else {
        gl_Position = ProjMat * ModelViewMat * vec4(Position, 1.0);
    }
}
