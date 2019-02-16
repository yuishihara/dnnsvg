from dnnsvg.svgeables.variables.variable import Variable
from dnnsvg.svgeables.svgeable import SVGeable
from dnnsvg.svgeables.shapes.text import Text
from dnnsvg.svgeables import svg_snippets


class Tensor2D(Variable):
    def __init__(self, x, y, height, width, color=(0, 0, 0), print_shape=True, draw_height=100, draw_width=5, dashed=False):
        super(Tensor2D, self).__init__(x, y, color)
        self._height = height
        self._width = width
        self._draw_height = draw_height
        self._draw_width = draw_width
        self._decorators = []
        self._dashed = dashed
        self._title = self._default_title() if print_shape else None

    def decorate(self, svgeable):
        if isinstance(svgeable, SVGeable):
            self._decorators.append(svgeable)

    def shape(self):
        return (self._height, self._width)

    def vertices(self):
        origin = self.origin()
        x, y = (origin[0],
                origin[1] - self._draw_height / 2.0)
        return [(x, y),
                (x + self._draw_width, y),
                (x, y + self._draw_height),
                (x + self._draw_width, y + self._draw_height)]

    def to_svg(self):
        origin = self.origin()
        x, y = (origin[0],
                origin[1] - self._draw_height / 2.0)
        tensor_2d_svg = svg_snippets.rectangle(point=(x, y),
                                               height=self._draw_height,
                                               width=self._draw_width,
                                               dashed=self._dashed)
        if self._title:
            tensor_2d_svg += self._title.to_svg()
        return tensor_2d_svg + ''.join(decorator.to_svg() for decorator in self._decorators)

    def _default_title(self):
        text = '{}'.format(int(self._width))
        text_size = 12
        margin = 3
        top_left_vertex = self.vertices()[0]
        top_right_vertex = self.vertices()[1]
        point = ((top_left_vertex[0] + top_right_vertex[0]) / 2.0,
                 top_left_vertex[1] - margin)
        return Text(point, text, size=text_size)
