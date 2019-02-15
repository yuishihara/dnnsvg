import math
import uuid


def header(height, width, x=0, y=0):
    header = '<svg xmlns="http://www.w3.org/2000/svg" ' \
        'xmlns:xlink="http://www.w3.org/1999/xlink" ' \
        'width= "{}" height="{}" '.format(width, height) + \
        'viewBox="{} {} {} {}">\n'.format(x, y, width, height)
    return header


def footer():
    footer = '</svg>'
    return footer


def line(point1, point2, stroke_width=1, dashed=False, color=(0, 0, 0), start_marker_id=None, end_marker_id=None):
    x1, y1 = point1
    x2, y2 = point2
    dash_array = 1 if dashed else None
    start_marker = 'marker-start="url(#{})"'.format(
        start_marker_id) if start_marker_id else ''
    end_marker = 'marker-end="url(#{})"'.format(
        end_marker_id) if end_marker_id else ''
    return '<line x1="{}" y1="{}" x2="{}" y2="{}" '\
        'stroke-width="{}" stroke-dasharray="{}" stroke="rgb{}" {} {}/>\n'.format(
            x1, y1, x2, y2, stroke_width, dash_array, color, start_marker, end_marker)


def arrow(point1, point2, stroke_width=1, dashed=False, color=(0, 0, 0), arrow_on_end=True, arrow_on_start=False):
    if arrow_on_start:
        start_marker_id = uuid.uuid4()
        start_marker = '<marker id="{}" viewBox="-5 -5 10 10" orient="auto">'.format(start_marker_id) + \
            '<polygon points="-5,-5 5,0 -5,5" fill="rgb{}" stroke="color{}" />'.format(color, color) + \
            '</marker>'
    else:
        start_marker_id = None
        start_marker = ''
    if arrow_on_end:
        end_marker_id = uuid.uuid4()
        end_marker = '<marker id="{}" viewBox="-5 -5 10 10" orient="auto">'.format(end_marker_id) + \
            '<polygon points="-5,-5 5,0 -5,5" fill="rgb{}" stroke="color{}" />'.format(color, color) + \
            '</marker>'
    else:
        end_marker_id = None
        end_marker = ''
    return ''.join([start_marker,
                    end_marker,
                    line(point1, point2, stroke_width=stroke_width, dashed=dashed, color=color, start_marker_id=start_marker_id, end_marker_id=end_marker_id)])


def rectangle(point, height, width, stroke_width=1, dashed=False, color=(0, 0, 0), fill=None):
    x, y = point
    dash_array = 5 if dashed else None
    fill_color = 'none' if fill is None else 'rgb{}'.format(color)
    return '<rect x="{}" y="{}" width="{}" height="{}" stroke-width="{}" stroke-dasharray="{}" stroke="rgb{}" fill="{}"/>'.format(x, y, width, height, stroke_width, dash_array, color, fill_color)


def rectangular(vertices, mirror=False, color=(0, 0, 0)):
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


def arc(start_point, end_point, radius, stroke_width=1, dashed=False, color=(0, 0, 0), fill=None,
        x_axis_rotation=0, large_arc=False, sweep=False, start_marker_id=None, end_marker_id=None):
    rx, ry = _pair(radius)
    sweep_flag = 1 if sweep else 0
    large_arc_flag = 1 if large_arc else 0
    dash_array = 5 if dashed else None
    fill_color = 'transparent' if fill is None else 'rgb{}'.format(color)
    start_marker = 'marker-start="url(#{})"'.format(
        start_marker_id) if start_marker_id else ''
    end_marker = 'marker-end="url(#{})"'.format(
        end_marker_id) if end_marker_id else ''
    return '<path d="M{} {} A {} {} {} {} {} {} {}" stroke-width="{}" stroke-dasharray="{}" stroke="rgb{}" fill="{}" {} {}/>' \
        .format(start_point[0], start_point[1], rx, ry, x_axis_rotation, large_arc_flag, sweep_flag, end_point[0], end_point[1], stroke_width, dash_array, color, fill_color, start_marker, end_marker)


def arc_arrow(start_point, end_point, radius, stroke_width=1, dashed=False, color=(0, 0, 0), fill=None,
              x_axis_rotation=0, large_arc=False, sweep=False, arrow_on_end=True, arrow_on_start=False):
    if arrow_on_start:
        start_marker_id = uuid.uuid4()
        start_marker = '<marker id="{}" viewBox="-5 -5 10 10" orient="auto">'.format(start_marker_id) + \
            '<polygon points="-5,-5 5,0 -5,5" fill="rgb{}" stroke="color{}" />'.format(color, color) + \
            '</marker>'
    else:
        start_marker_id = None
        start_marker = ''
    if arrow_on_end:
        end_marker_id = uuid.uuid4()
        end_marker = '<marker id="{}" viewBox="-5 -5 10 10" orient="auto">'.format(end_marker_id) + \
            '<polygon points="-5,-5 5,0 -5,5" fill="rgb{}" stroke="color{}" />'.format(color, color) + \
            '</marker>'
    else:
        end_marker_id = None
        end_marker = ''
    return ''.join([start_marker,
                    end_marker,
                    arc(start_point, end_point, radius, stroke_width, dashed, color, fill,
                        x_axis_rotation, large_arc, sweep, start_marker_id, end_marker_id)])


def text(point, contents, size=10, color=(0, 0, 0), anchor='middle'):
    x, y = point
    return '<text x="{}" y="{}" font-family="arial" font-size="{}px" '.format(x, y, size) + \
           'text-anchor="{}" fill="rgb{}">{}</text>\n'.format(
               anchor, color, contents)


def _pair(x):
    if hasattr(x, '__getitem__'):
        return x
    return x, x
