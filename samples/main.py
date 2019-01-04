from dnnsvg.layers import Convolution2D
from dnnsvg.layers import Deconvolution2D
from dnnsvg.layers import FullyConnected
from dnnsvg.layers import FullyConnectedLSTM
from dnnsvg.layers import Reshape
from dnnsvg.svgeables import Tensor3D
from dnnsvg import SVGBuilder


def main():
    width = 1280
    height = 480
    point = (50, height / 2.0)
    input_tensor = Tensor3D(x=point[0],
                            y=point[1],
                            depth=12,
                            height=120,
                            width=120)
    svg = SVGBuilder(height=height, width=width) \
        .add_layer(Convolution2D(in_channels=12, out_channels=64, ksize=6, stride=2)) \
        .add_layer(Convolution2D(in_channels=64, out_channels=128, ksize=4, stride=2)) \
        .add_layer(Reshape(output_shape=(1, 128*28*28))) \
        .add_layer(FullyConnectedLSTM(output_shape=(1, 2048))) \
        .add_layer(FullyConnected(output_shape=(1, 128*28*28))) \
        .add_layer(Reshape(output_shape=(128, 28, 28))) \
        .add_layer(Deconvolution2D(in_channels=128, out_channels=64, ksize=4, stride=2)) \
        .add_layer(Deconvolution2D(in_channels=64, out_channels=3, ksize=6, stride=2)) \
        .build(input_tensor)

    filename = 'sample.svg'
    with open(filename, 'w') as f:
        f.write(svg)


if __name__ == "__main__":
    main()