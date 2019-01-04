from dnnsvg.svgeables.svgeable import SVGeable
from dnnsvg.svgeables import svg_snippets


class ArcArrow(SVGeable):
    def __init__(self, point1, point2, radius, dashed=False, stroke_width=1, color=(0, 0, 0),
                 large_arc=True, sweep=False):
        super(ArcArrow, self).__init__()
        arrow_width = 5
        self._point1 = point1
        self._point2 = (point2[0] - arrow_width, point2[1])
        self._radius = radius
        self._dashed = dashed
        self._stroke_width = stroke_width
        self._color = color
        self._large_arc = large_arc
        self._sweep = sweep

    def to_svg(self):
        return svg_snippets.arc_arrow(start_point=self._point1,
                                      end_point=self._point2,
                                      radius=self._radius,
                                      stroke_width=self._stroke_width,
                                      dashed=self._dashed,
                                      color=self._color,
                                      large_arc=self._large_arc, 
                                      sweep=self._sweep)
