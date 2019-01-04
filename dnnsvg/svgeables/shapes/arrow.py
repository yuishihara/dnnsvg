from dnnsvg.svgeables.svgeable import SVGeable
from dnnsvg.svgeables import svg_snippets

class Arrow(SVGeable):
    def __init__(self, point1, point2, dashed=False, stroke_width=1, color=(0, 0, 0)):
        super(Arrow, self).__init__()
        arrow_width = 5
        self._point1 = point1
        self._point2 = (point2[0] - arrow_width, point2[1])
        self._dashed = dashed
        self._stroke_width = stroke_width
        self._color = color

    def to_svg(self):
        return svg_snippets.arrow(point1=self._point1,
                                  point2=self._point2,
                                  stroke_width=self._stroke_width,
                                  dashed=self._dashed,
                                  color=self._color)
