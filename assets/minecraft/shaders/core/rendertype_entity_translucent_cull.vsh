#version 150

#moj_import <light.glsl>

in vec3 Position;
in vec4 Color;
in vec2 UV0;
in vec2 UV1;
in ivec2 UV2;
in vec3 Normal;

uniform sampler2D Sampler2;

uniform mat4 ModelViewMat;
uniform mat4 ProjMat;

out float vertexDistance;
out vec4 vertexColor;
out vec2 texCoord0;
out vec2 texCoord1;
out vec2 texCoord2;
out vec4 normal;

void main() {
    gl_Position = ProjMat * ModelViewMat * vec4(Position, 1.0);

    vertexDistance = length((ModelViewMat * vec4(Position, 1.0)).xyz);
    if (UV2.y == 0) {
      vertexColor = minecraft_mix_light(vec3(1.0), vec3(1.0), Normal, Color) * texelFetch(Sampler2, ivec2(6), 0);
    } else {
      vertexColor = minecraft_mix_light(vec3(1.0), vec3(1.0), Normal, Color) * texelFetch(Sampler2, UV2 / 16, 0);
    }
    texCoord0 = UV0;
    texCoord1 = UV1;
    texCoord2 = UV2;
    normal = ProjMat * ModelViewMat * vec4(Normal, 0.0);
}
