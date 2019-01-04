from dnnsvg.layers.layer import Layer
from dnnsvg.layers.fully_connected import FullyConnected
from dnnsvg.svgeables import Tensor3D
from dnnsvg.svgeables import Line
from dnnsvg.svgeables import Text
from dnnsvg.svgeables import ArcArrow
import dnnsvg.svgeables
import math


class FullyConnectedLSTM(FullyConnected):
    def __init__(self, output_shape):
        super(FullyConnectedLSTM, self).__init__(output_shape)

    def decorate(self, input_tensor):
        output_tensor = super(FullyConnectedLSTM, self).decorate(input_tensor)
        arrow = self._recurrent_arrow(input_tensor)
        input_tensor.decorate(arrow)
        return output_tensor

    def _recurrent_arrow(self, input_tensor):
        left_vertices = self._left_vertices(input_tensor)
        right_vertices = self._right_vertices(input_tensor)
        pad = 5
        start_point = (right_vertices[0][0] + pad, right_vertices[0]
                       [1] * 0.4 + right_vertices[1][1] * 0.6)
        end_point = (left_vertices[0][0], left_vertices[0]
                     [1] * 0.4 + left_vertices[1][1] * 0.6)
        radius = 10
        return ArcArrow(start_point, end_point, radius, stroke_width=2, large_arc=True, sweep=True)

    def _layer_titles(self, input_tensor):
        text_size = 12
        title = 'fc_lstm'
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
