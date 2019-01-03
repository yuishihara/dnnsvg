from svgeable import SVGeable
import svg_snippets


class Line(SVGeable):
    def __init__(self, point1, point2, stroke_width=1, dashed=False, color=(0, 0, 0)):
        super(Line, self).__init__()
        self._point1 = point1
        self._point2 = point2
        self._stroke_width = stroke_width
        self._dashed = dashed
        self._color = color

    def to_svg(self):
        return svg_snippets.line(point1=self._point1,
                                 point2=self._point2,
                                 stroke_width=self._stroke_width,
                                 dashed=self._dashed,
                                 color=self._color)
