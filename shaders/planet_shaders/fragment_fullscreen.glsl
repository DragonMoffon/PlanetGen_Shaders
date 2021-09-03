#version 430

#define Pi 3.141592

struct planet
{
	vec2 pos;
	float radius;
	float mass;
};

layout(location = 0) uniform sampler2D planet_texture;

uniform vec4 camera_data;
uniform vec4 planet_data;

uniform float zoom;
uniform float time;

float earthTheta = 0.40840704496;
mat2 earthRotation = mat2(cos(earthTheta), -sin(earthTheta),
					      sin(earthTheta), cos(earthTheta));

float save = time;
vec3 lightDir = vec3(-cos(Pi*time/12), 0, sin(Pi*time/12));
//vec3 lightDir = vec3(-1, 0, 0);

in vec4 gl_FragCoord;

out vec4 fragColor;

void main() {
	vec2 true_pos = camera_data.xy + gl_FragCoord.xy*zoom;
	vec2 true_diff = planet_data.xy - true_pos;
	vec2 diff = true_diff * earthRotation;
	float dist = length(true_diff);

	fragColor = vec4(0);
	if (dist < planet_data.z)
	{
		float radius_width = sqrt(pow(planet_data.z, 2) - pow(diff.y, 2));
		float textureX = acos(diff.x/radius_width)/(2*Pi);
		float textureY = acos(diff.y/planet_data.z)/(Pi);

		vec2 normalXY = vec2(true_diff.x/planet_data.z, true_diff.y/planet_data.z);
		vec3 normalXYZ = vec3(normalXY, sqrt((pow(1, 2) - pow(normalXY.x, 2)) * (pow(1, 2) - pow(normalXY.y, 2))));

		float light_shift = clamp(dot(normalXYZ, lightDir), -1, 1)/2 + 0.5;
		float light_level = smoothstep(0.4, 0.6, light_shift);

		vec2 radial_pos = vec2(mod(textureX + planet_data.w/1440, 1),
							   textureY/2);
		//fragColor = texture(planet_texture, radial_pos);
		fragColor = mix(texture(planet_texture,
								clamp(radial_pos+vec2(0, 0.5), vec2(0, 0.5), vec2(1, 0.9999))),
								texture(planet_texture, radial_pos), light_level);
		//fragColor = vec4(vec3(light_shift), 1);
		//fragColor = mix(vec4(vec3(0), 1), vec4(1), light_level);
	}
}
