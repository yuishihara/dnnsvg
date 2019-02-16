from dnnsvg.svgeables.svgeable import SVGeable
from dnnsvg.svgeables import svg_snippets
from dnnsvg.svgeables.shapes.text import Text


class Caption(SVGeable):
    def __init__(self, point1, point2, title, text_size=10, dashed=False, stroke_width=1, color=(0, 0, 0)):
        super(Caption, self).__init__()
        self._point_left = point1
        self._point_right = point2
        self._title = title
        self._text_size = text_size
        self._dashed = dashed
        self._stroke_width = stroke_width
        self._color = color

    def to_svg(self):
        horizontal_line = svg_snippets.line(point1=self._point_left,
                                            point2=self._point_right,
                                            stroke_width=self._stroke_width,
                                            dashed=self._dashed,
                                            color=self._color)

        bar_size = 10 
        point_left_up = (self._point_left[0], self._point_left[1] + bar_size / 2.0)
        point_left_down = (self._point_left[0], self._point_left[1] - bar_size / 2.0)
        vertical_line_left = svg_snippets.line(point1=point_left_up,
                                            point2=point_left_down,
                                            stroke_width=self._stroke_width,
                                            dashed=self._dashed,
                                            color=self._color)
        point_right_up = (self._point_right[0], self._point_right[1] + bar_size / 2.0)
        point_right_down = (self._point_right[0], self._point_right[1] - bar_size / 2.0)
        vertical_line_right = svg_snippets.line(point1=point_right_up,
                                            point2=point_right_down,
                                            stroke_width=self._stroke_width,
                                            dashed=self._dashed,
                                            color=self._color)
        text_x = (self._point_left[0] + self._point_right[0]) / 2.0
        text_y = self._point_left[1] - 5
        text_position = (text_x, text_y)
        text = Text(point=text_position, text=self._title, size=self._title)
        return horizontal_line + vertical_line_left + vertical_line_right + text.to_svg()
