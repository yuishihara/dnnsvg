from layer_connector import LayerConnector
import svg_snippets


class LineConnector(LayerConnector):
    def __init__(self, point1, point2, stroke_width=1, dashed=False, color=(0, 0, 0)):
        super(LineConnector, self).__init__()
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
