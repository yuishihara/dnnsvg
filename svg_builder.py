import svg_snippets


class SVGBuilder(object):
    def __init__(self, height, width):
        self._height = height
        self._width = width
        self._layers = []

    def add_layer(self, layer):
        self._layers.append(layer)
        return self

    def build(self, input_tensor):
        svg_header = svg_snippets.header(height=self._height, width=self._width)
        svg_footer = svg_snippets.footer()
        tensors = [input_tensor]
        for layer in self._layers:
            out_tensor = layer(input_tensor)
            tensors.append(out_tensor)
            input_tensor = out_tensor
        svg_string = ''.join(tensor.to_svg() for tensor in tensors)
        return svg_header + svg_string + svg_footer
