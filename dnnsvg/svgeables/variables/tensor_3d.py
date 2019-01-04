from dnnsvg.svgeables.variables.variable import Variable
from dnnsvg.svgeables.svgeable import SVGeable
from dnnsvg.svgeables.shapes.text import Text
from dnnsvg.svgeables import svg_snippets
import math


class Tensor3D(Variable):
    def __init__(self, x, y, depth, height, width, scale, color=(0, 0, 0), mirror=False, print_shape=True):
        super(Tensor3D, self).__init__(x, y, color)
        self._depth = depth
        self._height = height
        self._width = width
        self._mirror = mirror
        self._angle = 2.0 / 3.0 * math.pi
        self._decorators = []
        self._d_scale, self._h_scale, self._w_scale = _pair(scale)
        self._title = self._default_title() if print_shape else None

    def decorate(self, svgeable):
        if isinstance(svgeable, SVGeable):
            self._decorators.append(svgeable)

    def shape(self):
        return (self._depth, self._height, self._width)

    def angle(self):
        return self._angle

    def vertices(self):
        origin = self.origin()
        depth = self._depth * self._d_scale
        height = self._height * self._h_scale
        width = self._width * self._w_scale
        x, y = (origin[0] - (width * math.cos(self._angle) / 2.0),
                origin[1] - (height + width * math.sin(self._angle)) / 2.0)
        angle = math.pi - self._angle if self._mirror else self._angle
        return [(x, y),
                (x+depth, y),
                (x, y+height),
                (x+depth, y+height),
                (x+width*math.cos(angle), y+width*math.sin(angle)),
                (x+depth+width*math.cos(angle), y+width*math.sin(angle)),
                (x+width*math.cos(angle), y + height+width*math.sin(angle)),
                (x+depth+width*math.cos(angle), y+height+width*math.sin(angle))]

    def scale(self):
        return (self._d_scale, self._h_scale, self._w_scale)

    def to_svg(self):
        tensor_3d_svg = svg_snippets.rectangular(vertices=self.vertices(),
                                                 mirror=self._mirror,
                                                 color=self.color())
        if self._title:
            tensor_3d_svg += self._title.to_svg()
        return tensor_3d_svg + ''.join(decorator.to_svg() for decorator in self._decorators)

    def _default_title(self):
        text = '{}x{}x{}'.format(int(self._depth),
                                 int(self._height),
                                 int(self._width))
        text_size = 10
        margin = 3
        top_left_vertex = self.vertices()[0]
        top_right_vertex = self.vertices()[1]
        point = ((top_left_vertex[0] + top_right_vertex[0]) / 2.0,
                 top_left_vertex[1] - margin)
        return Text(point, text, size=text_size)

def _pair(x):
    if hasattr(x, '__getitem__'):
        return x
    return x, x, x
