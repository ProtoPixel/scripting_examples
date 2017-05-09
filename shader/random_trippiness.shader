//https://www.shadertoy.com/view/lslGRj

int schedule = 0;

vec4 hue(float rad)
{
	rad /= 2.0;
	return vec4(abs(cos(rad)), abs(cos(rad+1.05)),
		abs(cos(rad+2.09)), 1.0);
}

vec4 gradient(float f)
{
	f = mod(f, 1.0) * 3.14;
	if (schedule == 0) {
		return vec4(sin(f) * sin(f));
	} else if (schedule == 1) {
		float r = pow(.5 + .5 * sin(2.0 * (f + 0.00)), 20.0);
		float g = pow(.5 + .5 * sin(2.0 * (f + 1.05)), 20.0);
		float b = pow(.5 + .5 * sin(2.0 * (f + 2.09)), 20.0);
		return vec4(r, g, b, 1.0);
	} else if (schedule == 2) {
		return vec4(0.0, .5+.5*sin(f), 0.0, 1.0);
	}
	return vec4(0.0);
}

float offset(float th)
{
	float mt = mod(iGlobalTime, 4.0);
	float x = sin(iGlobalTime + th) + sin(iGlobalTime + 2.0 * th)
		+ .3 * cos(iGlobalTime + 8.0 * th);
	if (schedule == 0) {
		return x + .2 * sin(10.0 * iGlobalTime + 20.0 * th);
	} else if (schedule == 1) {
		return x + floor(iGlobalTime * 3.0) * .333;
	} else if (schedule == 2) {
		return x + .1 * sin(60.0 * th);
	}
	return 0.0;
}

vec4 tunnel(float th, float radius)
{
	return gradient(offset(th) + log(6.0 * radius));
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
	vec2 uv = fragCoord.xy / iResolution.x +
		vec2(-.5, -.5 * iResolution.y / iResolution.x);
	schedule = int(mod(iGlobalTime + 2.0, 6.0) / 2.0);
	fragColor = tunnel(atan(uv.y, uv.x), 2.0 * length(uv));
}