from fully_connected import FullyConnected
from tensor_2d import Tensor2D
from line import Line
from text import Text
from arrow import Arrow
import math

class FullyConnectedLSTM(FullyConnected):
    def __init__(self, output_shape):
        super(FullyConnectedLSTM, self).__init__()
        if not len(output_shape) == 2:
            raise ValueError(
                "Shape must be 2D! Given shape: {}".format(output_shape))
        self._output_shape = output_shape

    def decorate(self, input_tensor):
        output_tensor = super(FullyConnectedLSTM, self).decorate(input_tensor)

        return output_tensor

    def _recurrent_arrow(self, input_tensor):
        pass

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
