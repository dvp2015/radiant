#version 330

uniform mat4 projection_matrix, model_view_matrix, normal_matrix, view_matrix;
uniform vec3 light_pos;

in vec3 pos;
in vec2 uv;
in vec3 normal;

out vec3 pos_viewspace;
out vec3 normal_viewspace;
out vec3 light_pos_viewspace;

void main() {
	gl_Position = projection_matrix * model_view_matrix * vec4(pos, 1.0);
	
	vec4 pos2 = model_view_matrix * vec4(pos, 1.0);
	pos_viewspace = vec3(pos2) / pos2.w;

	vec4 light_pos2 = view_matrix * vec4(light_pos, 1.0);
	light_pos_viewspace = vec3(light_pos2) / light_pos2.w;
	
	normal_viewspace = (normal_matrix * vec4(normal, 0.0)).xyz;
}
