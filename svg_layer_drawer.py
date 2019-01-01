class SvgLayerDrawer(object):
    def draw(self, point, input_shape, svgs):
        output_shape = self.draw_layer(point, input_shape, svgs)
        self.draw_title(point, svgs)
        return output_shape

    def draw_layer(self, point, input_shape, svgs):
        return input_shape

    def draw_title(self, point, svgs):
        pass
