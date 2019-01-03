from layer import Layer
from tensor_2d import Tensor2D
from tensor_3d import Tensor3D
import math


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

        return output_tensor

    def _output_tensor(self, input_tensor):
        if isinstance(input_tensor, Tensor3D):
            print('input tensor is 3D')
            in_depth, _, _ = input_tensor.shape()
            margin = in_depth
        elif isinstance(input_tensor, Tensor2D):
            print('input tensor is 2D')
            vertices = input_tensor.vertices()
            margin = (vertices[1][0] - vertices[0][0])

        point = input_tensor.origin()
        out_point = (point[0] + margin, point[1])
        if len(self._output_shape) == 2:
            out_height, out_width = self._output_shape
            margin = margin + 20
            out_point = (point[0] + margin, point[1])
            return Tensor2D(x=out_point[0],
                            y=out_point[1],
                            height=out_height,
                            width=out_width)
        elif len(self._output_shape) == 3:
            out_depth, out_height, out_width = self._output_shape
            margin = margin - out_width * math.cos(2.0 / 3.0 * math.pi)
            out_point = (point[0] + margin, point[1])
            return Tensor3D(x=out_point[0],
                            y=out_point[1],
                            depth=out_depth,
                            height=out_height,
                            width=out_width)
        else:
            raise ValueError(
                "Shape must be 2D or 3D! Given: {}".format(self._output_shape))

    def _assert_has_same_size(self, shape1, shape2):
        shape1_size = 1
        for count in shape1:
            shape1_size *= count

        shape2_size = 1
        for count in shape2:
            shape2_size *= count

        assert shape1_size == shape2_size
