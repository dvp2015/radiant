#version 330

in vec3 pos_viewspace;
in vec3 normal_viewspace;
in vec3 light_pos_viewspace;

uniform vec4 color;
uniform float shininess;

const vec4 specular_color = vec4(1.0, 1.0, 1.0, 1.0);


void main() {
	vec3 normal = normalize(normal_viewspace);
	vec3 light_dir = normalize(light_pos_viewspace - pos_viewspace);
	vec3 reflect_dir = reflect(-light_dir, normal);
	// the view direction is the vector to the fragment of the surface we are shading
	vec3 view_dir = normalize(-pos_viewspace);

	float lambertian = max(dot(light_dir, normal), 0.0);
	float specular = 0.0;

	// TODO: does this really need to be an if-statement? probably slow
	if (lambertian > 0.0) {
		float spec_angle = max(dot(reflect_dir, view_dir), 0.0);
		specular = pow(spec_angle, shininess);
	}

	gl_FragColor = lambertian * color + specular * specular_color;
}
