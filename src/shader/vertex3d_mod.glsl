// constant for all vertices
uniform float scale;
uniform float point_size;
uniform float offset_x;
uniform float offset_y;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
// attribute: input for each vertex
attribute vec3 color;
attribute vec3 position;
// interface between vertex and fragment shader, is interpolated on polygon
varying vec4 v_color;
void main()
{
    position[0] += offset_x;
    position[1] += offset_y;
    gl_PointSize = point_size;
    v_color = vec4(color/255, 1.0);
    gl_Position = projection * view * model *  vec4(scale * position, 1.0);
    //gl_Position = projection *  vec4(scale*position, 0.0, 1.0);
    //gl_Position = vec4(scale*position, 0.0, 1.0);
    //gl_Position = vec4(position, 0.0, 1.0);
}