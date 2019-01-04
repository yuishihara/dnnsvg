from dnnsvg.svgeables.svgeable import SVGeable


class Variable(SVGeable):
    def __init__(self, x, y, color):
        super(Variable, self).__init__()
        self._x = x
        self._y = y
        self._color = color

    def origin(self):
        return (self._x, self._y)

    def color(self):
        return self._color

    def vertices(self):
        raise NotImplementedError("vertices() not implemented")

    def decorate(self, svgeable):
        raise NotImplementedError('decorate() not implemented')

    def shape(self):
        raise NotImplementedError('shape() not implemented')
