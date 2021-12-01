#version 150

in vec3 Position;

uniform mat4 ModelViewMat;
uniform mat4 ProjMat;

out float vertexDistance;

void main() {
    gl_Position = ProjMat * ModelViewMat * vec4(Position.x, Position.y/100, Position.z, 1);

    vertexDistance = length((ModelViewMat * vec4(Position, 1.0)).xyz);
}