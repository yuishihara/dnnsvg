import svg_snippets
from convolution_2d import Convolution2D
from deconvolution_2d import Deconvolution2D


def main():
    width = 1280
    height = 480
    layers = [Convolution2D(in_channels=3, out_channels=64, ksize=6, stride=2),
              Convolution2D(in_channels=64, out_channels=128,
                            ksize=4, stride=2),
              Deconvolution2D(in_channels=128, out_channels=64,
                              ksize=4, stride=2),
              Deconvolution2D(in_channels=64, out_channels=3, ksize=6, stride=2)]

    svg_header = svg_snippets.header(height=height, width=width)
    svg_footer = svg_snippets.footer()

    point = (50, 100)
    prev_shape = (0, 0, 0)
    input_shape = (3, 120, 120)
    svgs = []
    margin = 40
    for layer in layers:
        point = (point[0] + prev_shape[0] + margin, point[1])
        prev_shape = input_shape
        next_shape = layer.draw(point, input_shape, svgs)
        input_shape = next_shape
    svg_string = ''.join(svg for svg in svgs)

    filename = 'sample.svg'
    with open(filename, 'w') as f:
        f.write(svg_header + svg_string + svg_footer)


if __name__ == "__main__":
    main()
