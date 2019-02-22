# version 460
// constant for all vertices
uniform float scale;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform float width;
uniform float height;

in vec2 position; // input for each vertex
out vec2 texture_point; // is interpolated between vertices
void main()
{
    vec2 temp;
    vec2 temp2;
    if(position[0] > 0.0)
    {
        temp[0] = 1.0;
        temp2[0] = width;
    }else{
        temp[0] = 0.0;
        temp2[0] = -width;
    }
    if(position[1] > 0.0)
    {
        temp[1] = 1.0;
        temp2[1] = 1.0;
    }else{
        temp[1] = 0.0;
        temp2[1] = -height;
    }

    texture_point = vec2(temp[0], 1.0 - temp[1]);

    gl_Position =  projection * view * model *vec4(scale * (temp2), 0.0, 1.0);


}