from dnnsvg.layers.layer import Layer
from dnnsvg.svgeables import Tensor3D
from dnnsvg.svgeables import Tensor2D
from dnnsvg.svgeables import Text
from dnnsvg.svgeables import Arrow
import dnnsvg.svgeables


class Reshape(Layer):
    def __init__(self, output_shape):
        super(Reshape, self).__init__()
        if not len(output_shape) == 2 and not len(output_shape) == 3:
            raise ValueError(
                "Shape must be 2D or 3D! Given: {}".format(output_shape))
        self._output_shape = output_shape

    def decorate(self, input_tensor):
        input_shape = input_tensor.shape()
        output_shape = self._output_shape
        self._assert_has_same_size(input_shape, output_shape)

        output_tensor = self._output_tensor(input_tensor)

        titles = self._layer_titles(input_tensor)
        for title in titles:
            input_tensor.decorate(title)

        connector = self._input_output_connector(input_tensor, output_tensor)
        input_tensor.decorate(connector)
        return output_tensor

    def _output_tensor(self, input_tensor):
        if isinstance(input_tensor, Tensor3D):
            in_depth, _, _ = input_tensor.shape()
            width = in_depth
            margin = self._inter_layer_margin()
        elif isinstance(input_tensor, Tensor2D):
            vertices = input_tensor.vertices()
            width = (vertices[1][0] - vertices[0][0])
            margin = self._inter_layer_margin()

        point = input_tensor.origin()
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
            return Tensor3D(x=out_point[0],
                            y=out_point[1],
                            depth=out_depth,
                            height=out_height,
                            width=out_width)
        else:
            raise ValueError(
                "Shape must be 2D or 3D! Given: {}".format(self._output_shape))

    def _input_output_connector(self, input_tensor, output_tensor):
        start_point = None
        end_point = None
        input_vertices = self._right_vertices(input_tensor)

        input_origin = input_tensor.origin()

        start_padding = 5
        if isinstance(input_tensor, Tensor3D):
            start_point = ((input_vertices[0][0] + input_vertices[1][0]) / 2.0 + start_padding,
                           input_origin[1])
        elif isinstance(input_tensor, Tensor2D):
            start_point = ((input_vertices[0][0] + input_vertices[1][0]) / 2.0 + start_padding,
                           input_origin[1])

        end_padding = 5
        output_origin = output_tensor.origin()
        output_vertices = self._left_vertices(output_tensor)
        if isinstance(output_tensor, Tensor3D):
            end_point = ((output_vertices[2][0] + output_vertices[3][0]) / 2.0 - end_padding,
                         output_origin[1])
        elif isinstance(output_tensor, Tensor2D):
            end_point = ((output_vertices[0][0] + output_vertices[1][0]) / 2.0 - end_padding,
                         output_origin[1])

        return Arrow(point1=start_point, point2=end_point, stroke_width=2)

    def _layer_titles(self, input_tensor):
        text_size = 12
        title = 'reshape'
        texts = [title]

        input_vertices = self._left_vertices(input_tensor)
        if isinstance(input_tensor, Tensor2D):
            base_text_point = (input_vertices[1][0], input_vertices[1][1] + 10)
        elif isinstance(input_tensor, Tensor3D):
            base_text_point = (input_vertices[3][0], input_vertices[3][1] + 10)
        titles = []
        for i, text in enumerate(texts):
            text_point = (base_text_point[0],
                          base_text_point[1] + i * text_size)
            titles.append(
                Text(text_point, text, size=text_size, anchor='left'))
        return titles

    def _assert_has_same_size(self, shape1, shape2):
        shape1_size = 1
        for count in shape1:
            shape1_size *= count

        shape2_size = 1
        for count in shape2:
            shape2_size *= count

        assert shape1_size == shape2_size
