from dnnsvg.layers.layer import Layer
from dnnsvg.svgeables import Tensor2D
from dnnsvg.svgeables import Tensor3D
from dnnsvg.svgeables import Line
from dnnsvg.svgeables import Text
from dnnsvg.svgeables import Arrow
import dnnsvg.svgeables
import math


class CustomLayer(Layer):
    def __init__(self, output_shape, output_scale,
                 layer_height, layer_width, layer_name, dashed=True):
        super(CustomLayer, self).__init__()
        self._output_shape = output_shape
        self._output_scale = output_scale
        self._layer_height = layer_height
        self._layer_width = layer_width
        self._layer_name = layer_name
        self._dashed=dashed

    def decorate(self, input_tensor):
        layer_tensor = self._layer_tensor(input_tensor)
        input_tensor.decorate(layer_tensor)

        output_tensor = self._output_tensor(layer_tensor)

        titles = self._layer_titles(layer_tensor)
        for title in titles:
            layer_tensor.decorate(title)

        connectors = self._input_output_connectors(input_tensor, layer_tensor)
        connectors.extend(self._input_output_connectors(layer_tensor, output_tensor))
        for connector in connectors:
            input_tensor.decorate(connector)
        return output_tensor

    def _layer_tensor(self, input_tensor):
        vertices = input_tensor.vertices()
        width = (vertices[1][0] - vertices[0][0])
        margin = self._inter_layer_margin()

        point = input_tensor.origin()
        out_point = (point[0] + width + margin, point[1])

        return Tensor2D(x=out_point[0],
                        y=out_point[1],
                        height=self._layer_height,
                        width=self._layer_width,
                        draw_height=self._layer_height,
                        draw_width=self._layer_width,
                        print_shape=False,
                        dashed=self._dashed)

    def _output_tensor(self, layer_tensor):
        vertices = layer_tensor.vertices()
        width = (vertices[1][0] - vertices[0][0])
        margin = self._inter_layer_margin()

        point = layer_tensor.origin()
        out_point = (point[0] + width + margin, point[1])
        if len(self._output_shape) == 2:
            out_height, out_width = self._output_shape
            out_point = (point[0] + width + margin, point[1])
            return Tensor2D(x=out_point[0],
                            y=out_point[1],
                            height=out_height,
                            width=out_width)
        elif len(self._output_shape) == 3:
            out_depth, out_height, out_width = self._output_shape
            out_point = (point[0] + width + margin, point[1])
            scale = self._output_scale if self._output_scale else layer_tensor.scale()
            return Tensor3D(x=out_point[0],
                            y=out_point[1],
                            depth=out_depth,
                            height=out_height,
                            width=out_width,
                            scale=scale)
        else:
            raise ValueError(
                "Shape must be 2D or 3D! Given: {}".format(self._output_shape))

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
        return [arrow]

    def _layer_titles(self, input_tensor):
        text_size = self._text_size()
        title = self._layer_name
        texts = [title]

        left_vertices = self._left_vertices(input_tensor)
        right_vertices = self._right_vertices(input_tensor)
        base_text_point = ((left_vertices[1][0] + right_vertices[1][0]) / 2.0, left_vertices[1][1] + 10)
        titles = []
        for i, text in enumerate(texts):
            text_point = (base_text_point[0],
                          base_text_point[1] + i * text_size)
            titles.append(
                Text(text_point, text, size=text_size, anchor='middle'))
        return titles
