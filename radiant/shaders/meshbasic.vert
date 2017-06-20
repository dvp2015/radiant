#version 330

uniform mat4 mvp;

in vec3 in_vert;

void main() {
	gl_Position = mvp * vec4(v_vert, 1.0);
}
