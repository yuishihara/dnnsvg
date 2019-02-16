from dnnsvg.layers.tensor_decorator import TensorDecorator
from dnnsvg.svgeables import Tensor3D
from dnnsvg.svgeables import Tensor2D
import math


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

    @classmethod
    def _text_size(self):
        return 14