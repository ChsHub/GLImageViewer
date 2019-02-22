# version 460
in vec2 texture_point;
out vec4 frag_color;
uniform sampler2D ourTexture;

void main()
{
    frag_color = texture(ourTexture, texture_point); // Get pixel for 2D postion
}