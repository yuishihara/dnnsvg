import svg_snippets
from convolution_2d import Convolution2D
from deconvolution_2d import Deconvolution2D
from reshape import Reshape
from tensor_3d import Tensor3D


def main():
    width = 640
    height = 480
    layers = [Convolution2D(in_channels=12, out_channels=64, ksize=6, stride=2),
              Convolution2D(in_channels=64, out_channels=128, ksize=4, stride=2),
              Reshape(output_shape=(1, 128*28*28)),
              Reshape(output_shape=(128, 28, 28)),
              Deconvolution2D(in_channels=128, out_channels=64, ksize=4, stride=2),
              Deconvolution2D(in_channels=64, out_channels=3, ksize=6, stride=2)]   
    svg_header = svg_snippets.header(height=height, width=width)
    svg_footer = svg_snippets.footer()

    point = (50, height / 2.0)
    input_tensor = Tensor3D(x=point[0],
                            y=point[1],
                            depth=12,
                            height=120,
                            width=120)
    tensors = [input_tensor]
    for layer in layers:
        out_tensor = layer(input_tensor)
        tensors.append(out_tensor)
        input_tensor = out_tensor
    svg_string = ''.join(tensor.to_svg() for tensor in tensors)

    filename = 'sample.svg'
    with open(filename, 'w') as f:
        f.write(svg_header + svg_string + svg_footer)


if __name__ == "__main__":
    main()
