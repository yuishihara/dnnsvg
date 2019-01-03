from svgeable import SVGeable
import svg_snippets


class Text(SVGeable):
    def __init__(self, point, text, size=10, color=(0, 0, 0), anchor='middle'):
        super(Text, self).__init__()
        self._point = point
        self._text = text
        self._size = size
        self._color = color
        self._anchor = anchor

    def to_svg(self):
        return svg_snippets.text(point=self._point,
                                 contents=self._text, 
                                 size=self._size, 
                                 color=self._color,
                                 anchor=self._anchor)
