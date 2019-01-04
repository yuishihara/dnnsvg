from dnnsvg.layers import Convolution2D
from dnnsvg.layers import Deconvolution2D
from dnnsvg.layers import FullyConnected
from dnnsvg.layers import FullyConnectedLSTM
from dnnsvg.layers import MaxPooling
from dnnsvg.layers import Reshape
from dnnsvg import Tensor3D
from dnnsvg import SVGBuilder

import argparse


def write_svg_to_file(filename, svg):
    with open(filename, 'w') as f:
        f.write(svg)

def alexnet():
    width = 900
    height = 480
    initial_position = (50, height / 2.0)
    input_tensor = Tensor3D(x=initial_position[0],
                            y=initial_position[1],
                            depth=3,
                            height=227,
                            width=227,
                            scale=(0.1, 0.6, 0.6))
    svg = SVGBuilder(height=height, width=width) \
        .add_layer(Convolution2D(in_channels=None, out_channels=96, ksize=11, stride=4)) \
        .add_layer(MaxPooling(ksize=3, stride=2)) \
        .add_layer(Convolution2D(in_channels=96, out_channels=256, ksize=5, stride=1, pad=2)) \
        .add_layer(MaxPooling(ksize=3, stride=2)) \
        .add_layer(Convolution2D(in_channels=256, out_channels=384, ksize=3, stride=1, pad=1)) \
        .add_layer(Convolution2D(in_channels=384, out_channels=384, ksize=3, stride=1, pad=1)) \
        .add_layer(Convolution2D(in_channels=384, out_channels=256, ksize=3, stride=1, pad=1)) \
        .add_layer(MaxPooling(ksize=3, stride=2)) \
        .add_layer(Reshape(output_shape=(1, 9216))) \
        .add_layer(FullyConnected(output_shape=(1, 4096))) \
        .add_layer(FullyConnected(output_shape=(1, 4096))) \
        .add_layer(FullyConnected(output_shape=(1, 1000))) \
        .build(input_tensor)

    filename = 'alexnet.svg'
    write_svg_to_file(filename, svg)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--alexnet', action='store_true')

    args = parser.parse_args()

    if args.alexnet:
        alexnet()

    alexnet()


if __name__ == "__main__":
    main()
