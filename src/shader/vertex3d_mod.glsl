# version 460
// constant for all vertices
uniform float scale;
uniform float offset_x;
uniform float offset_y;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

in vec2 position; // input for each vertex
out vec2 texture_point; // is interpolated between vertices
void main()
{
    texture_point = position; // vec2(position[0], position[1]);
    gl_Position = projection * view * model *  vec4(scale * position, 0.0, 1.0);

}