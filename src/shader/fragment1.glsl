# version 460
in vec2 texture_point;
out vec4 frag_color;
uniform sampler2D ourTexture;
void main()
{
    frag_color = vec4(texture_point,0.0,1.0);//texture(ourTexture, texture_point);
}