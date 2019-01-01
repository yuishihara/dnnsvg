from svg_layer_drawer import SvgLayerDrawer
import svg_snippets
import math


class Deconvolution2D(SvgLayerDrawer):
    def __init__(self, in_channels, out_channels, ksize=None, stride=1, pad=0):
        super(Deconvolution2D, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.k_size = _pair(ksize)
        self.stride = _pair(stride)
        self.pad = _pair(pad)

    def draw_layer(self, point, input_shape, svgs):
        in_channels, in_height, in_width = input_shape
        if self.in_channels is None:
            self.in_channels = in_channels
        if self.out_channels is None:
            self.out_channels = self.in_channels
        out_height = (in_height - 1) * \
            self.stride[0] + self.k_size[0] - 2 * self.pad[0]
        out_width = (in_width - 1) * \
            self.stride[1] + self.k_size[0] - 2 * self.pad[0]

        angle = 2.0 * math.pi / 3.0
        layer_point = (point[0] - in_width * math.cos(math.pi - angle) / 2.0,
                       point[1] - in_height / 2.0)
        svgs.append(svg_snippets.rectangular(
            layer_point, height=in_height, width=in_width, depth=in_channels, angle=angle, mirror=True))

        kernel_height = self.k_size[0]
        kernel_width = self.k_size[1]
        kernel_point = (point[0] - kernel_width * math.cos(math.pi - angle) / 2.0,
                        point[1] + in_height / 2.0 - kernel_height)
        svgs.append(svg_snippets.rectangular(
            kernel_point, height=kernel_height, width=kernel_width, depth=in_channels, angle=angle, mirror=True))

        return (self.out_channels, out_height, out_width)

    def draw_title(self, point, svgs):
        pass


def _pair(x):
    if hasattr(x, '__getitem__'):
        return x
    return x, x
