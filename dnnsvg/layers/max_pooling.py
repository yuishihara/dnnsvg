from dnnsvg.layers.layer import Layer
from dnnsvg.svgeables import Tensor3D
from dnnsvg.svgeables import Line
from dnnsvg.svgeables import Text
import dnnsvg.svgeables
import math


class MaxPooling(Layer):
    def __init__(self, ksize=None, stride=1):
        super(MaxPooling, self).__init__()
        self.k_size = _pair(ksize)
        self.stride = _pair(stride)
        self.pad = _pair(0)

    def decorate(self, input_tensor):
        input_shape = input_tensor.shape()
        if len(input_shape) is not 3:
            raise ValueError('Input must be 3D tensor!')

        # Decorate input tensor with kernel tensor (a.k.a filter)
        kernel_tensor = self._kernel_tensor(input_tensor)
        input_tensor.decorate(kernel_tensor)

        # Output tensor
        output_tensor = self._output_tensor(input_tensor)

        # Connect input_tensor and output_tensor with lines by decorating input_tensor
        connectors = self._input_output_connectors(
            input_tensor, output_tensor, kernel_tensor)
        for connector in connectors:
            input_tensor.decorate(connector)

        # Add layer title
        layer_titles = self._layer_titles(input_tensor)
        for title in layer_titles:
            input_tensor.decorate(title)

        return output_tensor

    def _kernel_tensor(self, input_tensor):
        input_shape = input_tensor.shape()
        if len(input_shape) is not 3:
            raise ValueError('Input must be 3D tensor!')
        in_depth, _, _ = input_shape
        in_channels = in_depth

        point = input_tensor.origin()
        # Decorate input tensor with kernel tensor (a.k.a filter)
        kernel_depth = in_channels
        kernel_height = self.k_size[0]
        kernel_width = self.k_size[1]
        kernel_point = point
        kernel_color = (0, 0, 255)
        return Tensor3D(x=kernel_point[0],
                        y=kernel_point[1],
                        depth=kernel_depth,
                        height=kernel_height,
                        width=kernel_width,
                        color=kernel_color,
                        print_shape=False)

    def _output_tensor(self, input_tensor):
        input_shape = input_tensor.shape()
        if len(input_shape) is not 3:
            raise ValueError('Input must be 3D tensor!')
        in_depth, _, _ = input_shape
        out_channels = in_depth

        point = input_tensor.origin()
        in_depth, in_height, in_width = input_tensor.shape()
        # Output tensor
        out_depth = out_channels
        out_height = (in_height + 2 *
                      self.pad[0] - self.k_size[0]) / self.stride[0] + 1
        out_width = (in_width + 2 *
                     self.pad[1] - self.k_size[1]) / self.stride[1] + 1

        margin = self._inter_layer_margin()
        out_point = (point[0] + in_depth + margin, point[1])
        return Tensor3D(x=out_point[0],
                        y=out_point[1],
                        depth=out_depth,
                        height=out_height,
                        width=out_width)

    def _input_output_connectors(self, input_tensor, output_tensor, kernel_tensor):
        kernel_vertices = self._right_vertices(kernel_tensor)
        output_vertices = self._left_vertices(output_tensor)
        destination_x = (output_vertices[0][0] * 0.75
                         + output_vertices[3][0] * 0.25)
        destination_y = (output_vertices[0][1] * 0.75
                         + output_vertices[3][1] * 0.25)
        destination_point = (destination_x, destination_y)
        kernel_color = kernel_tensor.color()
        return [Line(kernel_vertices[0], destination_point, color=kernel_color, dashed=True),
                Line(kernel_vertices[1], destination_point,
                     color=kernel_color, dashed=True),
                Line(kernel_vertices[2], destination_point,
                     color=kernel_color, dashed=True),
                Line(kernel_vertices[3], destination_point, color=kernel_color, dashed=True)]

    def _layer_titles(self, input_tensor):
        text_size = 12
        title = 'max pool'
        kernel_text = 'kernel:{}'.format(self.k_size)
        stride_text = 'stride:{}'.format(self.stride)
        texts = [title, kernel_text, stride_text]

        input_vertices = self._left_vertices(input_tensor)
        base_text_point = (input_vertices[3][0], input_vertices[3][1] + 10)
        titles = []
        for i, text in enumerate(texts):
            text_point = (base_text_point[0],
                          base_text_point[1] + i * text_size)
            titles.append(
                Text(text_point, text, size=text_size, anchor='left'))
        return titles


def _pair(x):
    if hasattr(x, '__getitem__'):
        return x
    return x, x
