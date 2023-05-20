// This code can be found in 
// https://www.shadertoy.com/view/XsSyWw
// and it's property of its creator.
// This is distributed for illustration purposes only.
// HSL colorspace:
vec3 hsl2rgb( in vec3 c )
{
    vec3 rgb = clamp( abs(mod(c.x*6.0+vec3(0.0,4.0,2.0),6.0)-3.0)-1.0, 0.0, 1.0 );

    return c.z + c.y * (rgb-0.5)*(1.0-abs(2.0*c.z-1.0));
}


// GLSL Tutorial for reference:
// https://www.shadertoy.com/view/Md23DV
void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    
    // Coordinate to width:
    vec2 p = vec2(fragCoord.xy / iResolution.xy);
    
    // Number of tiles across
    float tiles = 4.0;
    
    // Project point into that tile
    vec2 tp = p * tiles;
    
    // Determine the spin of that tile
    float sx = floor(mod(tp.x, 2.0)) * 2.0 - 1.0;
    float sy = floor(mod(tp.y, 2.0)) * 2.0 - 1.0;
    float spin = sx * sy;
    
    // Normalize the tile point
    vec2 coord = mod(tp, 1.0) * iResolution.xy;
     
    // Just an alias for no reason
    vec3 res = iResolution;
            
    // Polar coordinates:
    // https://www.shadertoy.com/view/ltlXRf
    vec2 rel = coord.xy - (res.xy / 2.0);
    vec2 polar;
    polar.y = sqrt(rel.x * rel.x + rel.y * rel.y);
    polar.y /= res.x / 2.0;
    polar.y = 1.0 - polar.y;

    polar.x = atan(rel.y, rel.x);
    polar.x -= 1.57079632679;
    if(polar.x < 0.0){
		polar.x += 6.28318530718;
    }
    polar.x /= 6.28318530718;
    polar.x = 1.0 - polar.x;
    
    // Visualization params:
    float speed = 0.3;
    float arms = 1.0;
    //float tightness = (sin(iTime * 2.0 / 3.0) + 1.0) * 0.5 * arms + 0.5;
    float tightness = 1.5 * arms;
    
    // Compute swirl:
    float hue = spin * polar.x * arms
        + mod(arms, 2.0) * sy * 0.25
        + iTime * speed
        + spin * rel.x * rel.y / res.x / res.y * tightness;

    // Compute rgb:
    vec3 rgb = hsl2rgb(vec3(hue, 1.0, 0.6));
    fragColor = vec4(rgb, 1.0);
    
    
}