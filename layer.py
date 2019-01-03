from tensor_decorator import TensorDecorator
from tensor_2d import Tensor2D
from tensor_3d import Tensor3D


class Layer(TensorDecorator):
    def __init__(self):
        super(Layer, self).__init__()

    @classmethod
    def _inter_layer_margin(self):
        return 50

    @classmethod
    def _left_vertices(self, tensor):
        vertices = tensor.vertices()
        if isinstance(tensor, Tensor3D):
            return [vertices[0], vertices[2], vertices[4], vertices[6]]
        elif isinstance(tensor, Tensor2D):
            return [vertices[0], vertices[2]]

    @classmethod
    def _right_vertices(self, tensor):
        vertices = tensor.vertices()
        if isinstance(tensor, Tensor3D):
            return [vertices[1], vertices[3], vertices[5], vertices[7]]
        elif isinstance(tensor, Tensor2D):
            return [vertices[1], vertices[3]]
