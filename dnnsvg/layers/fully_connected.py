from dnnsvg.layers.layer import Layer
from dnnsvg.svgeables import Tensor2D
from dnnsvg.svgeables import Line
from dnnsvg.svgeables import Text
from dnnsvg.svgeables import Arrow
import dnnsvg.svgeables
import math

class FullyConnected(Layer):
    def __init__(self, output_shape):
        super(FullyConnected, self).__init__()
        if not len(output_shape) == 2:
            raise ValueError(
                "Shape must be 2D! Given shape: {}".format(output_shape))
        self._output_shape = output_shape

    def decorate(self, input_tensor):
        assert isinstance(input_tensor, Tensor2D)

        output_tensor = self._output_tensor(input_tensor)

        titles = self._layer_titles(input_tensor)
        for title in titles:
            input_tensor.decorate(title)

        connectors = self._input_output_connectors(input_tensor, output_tensor)
        for connector in connectors:
            input_tensor.decorate(connector)
        return output_tensor

    def _output_tensor(self, input_tensor):
        _, input_size = input_tensor.shape()
        vertices = input_tensor.vertices()
        width = (vertices[1][0] - vertices[0][0])
        height = math.fabs(vertices[1][1] - vertices[3][1])
        margin = self._inter_layer_margin()

        point = input_tensor.origin()
        out_height, out_width = self._output_shape
        out_size = out_width
        out_point = (point[0] + width + margin, point[1])
        out_point = (point[0] + width + margin, point[1])

        draw_height = (out_size / input_size) * height
        return Tensor2D(x=out_point[0],
                        y=out_point[1],
                        height=out_height,
                        width=out_width,
                        draw_height=draw_height)

    def _input_output_connectors(self, input_tensor, output_tensor):
        start_point = None
        end_point = None
        input_vertices = self._right_vertices(input_tensor)

        input_origin = input_tensor.origin()

        start_padding = 5
        start_top_vertex = input_vertices[0]
        start_bottom_vertex = input_vertices[1]
        start_point = ((start_top_vertex[0] + start_bottom_vertex[0]) / 2.0 + start_padding,
                       input_origin[1])

        end_padding = 5
        output_origin = output_tensor.origin()
        output_vertices = self._left_vertices(output_tensor)
        end_top_vertex = output_vertices[0]
        end_bottom_vertex = output_vertices[1]
        end_point = ((end_top_vertex[0] + end_bottom_vertex[0]) / 2.0 - end_padding,
                     output_origin[1])
        arrow = Arrow(point1=start_point, point2=end_point, stroke_width=2)
        lines = [Line(point1=start_top_vertex, point2=end_top_vertex, dashed=True),
                 Line(point1=start_bottom_vertex, point2=end_bottom_vertex, dashed=True)]
        return [arrow] + lines

    def _layer_titles(self, input_tensor):
        text_size = 12
        title = 'fc'
        texts = [title]

        input_vertices = self._left_vertices(input_tensor)
        base_text_point = (input_vertices[1][0], input_vertices[1][1] + 10)
        titles = []
        for i, text in enumerate(texts):
            text_point = (base_text_point[0],
                          base_text_point[1] + i * text_size)
            titles.append(
                Text(text_point, text, size=text_size, anchor='left'))
        return titles
