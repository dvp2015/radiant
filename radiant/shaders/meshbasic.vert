#version 330

uniform mat4 projection_matrix, model_view_matrix;

in vec3 pos;

void main() {
	gl_Position = projection_matrix * model_view_matrix * vec4(pos, 1.0);
}
