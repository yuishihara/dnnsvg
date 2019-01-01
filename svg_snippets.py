import math


def header(height, width, x=0, y=0):
    header = '<svg xmlns="http://www.w3.org/2000/svg" ' \
        'xmlns:xlink="http://www.w3.org/1999/xlink" ' \
        'width= "{}" height="{}" '.format(width, height) + \
        'viewBox="{} {} {} {}">\n'.format(x, y, width, height)
    return header


def footer():
    footer = '</svg>'
    return footer


def line(point1, point2, stroke_width=1, dashed=False, color=(0, 0, 0)):
    x1, y1 = point1
    x2, y2 = point2
    dash_array = 5 if dashed else None
    return '<line x1="{}" y1="{}" x2="{}" y2="{}" '\
        'stroke-width="{}" stroke-dasharray="{}" stroke="rgb{}"/>\n'.format(
            x1, y1, x2, y2, stroke_width, dash_array, color)


def rectangle(point, height, width, stroke_width=1, dashed=False, color=(0, 0, 0), fill=None):
    x, y = point
    dash_array = 5 if dashed else None
    fill_color = 'transparent' if fill is None else 'rgb{}'.format(fill)
    return '<rect x="{}" y="{}" width="{}" height="{}" stroke-width="{}" stroke-dasharray="{}" stroke="rgb{}" fill="{}"/>' \
        .format(x, y, width, height, stroke_width, dash_array, color, fill_color)


def rectangular(point, height, width, depth, color=(0, 0, 0), mirror=False):
    x, y = point
    angle = math.pi / 3.0 if mirror else 2.0 * math.pi / 3.0
    vertices = [(x, y),
                (x+depth, y),
                (x, y+height),
                (x+depth, y+height),
                (x+width*math.cos(angle), y+width*math.sin(angle)),
                (x+depth+width*math.cos(angle), y+width*math.sin(angle)),
                (x+width*math.cos(angle), y+height+width*math.sin(angle)),
                (x+depth+width*math.cos(angle), y+height+width*math.sin(angle))]
    edges = [line(vertices[0], vertices[1], color=color),  # -
             line(vertices[0], vertices[2], color=color,
                  dashed=(not mirror)),  # |
             line(vertices[1], vertices[3], color=color, dashed=(mirror)),  # |
             line(vertices[2], vertices[3], color=color, dashed=True),  # -
             line(vertices[0], vertices[4], color=color),  # \ or /
             line(vertices[1], vertices[5], color=color),  # \ or /
             line(vertices[4], vertices[5], color=color),  # -
             line(vertices[4], vertices[6], color=color),  # |
             line(vertices[5], vertices[7], color=color),  # |
             line(vertices[6], vertices[7], color=color),  # -
             line(vertices[2], vertices[6], color=color,
                  dashed=(not mirror)),  # \ or /
             line(vertices[3], vertices[7], color=color, dashed=(mirror))]  # \ or /
    return ''.join(edges)


def text(point, contents, size=10, color=(0, 0, 0)):
    x, y = point
    return '<text x="{}" y="{}" font-family="arial" font-size="{}px" '.format(x, y, size) + \
           'text-anchor="middle" fill="rgb{}">{}</text>\n'.format(
               color, contents)
