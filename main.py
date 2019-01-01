import svg_snippets


def main():
    width = 640
    height = 480
    svg_header = svg_snippets.header(height=height, width=width)
    svg_footer = svg_snippets.footer()
    svgs = [svg_snippets.line((0, 100), (100, 100)),
            svg_snippets.line((100, 100), (100, 200), dashed=True),
            svg_snippets.text((100, 150), 'hello world'),
            svg_snippets.rectangle(
                (400, 100), height=100, width=50, dashed=True),
            svg_snippets.rectangle(
                (400, 200), height=100, width=50, dashed=True, fill=(255, 0, 0)),
            svg_snippets.rectangular(
                (200, 200), height=150, width=100, depth=10),
            svg_snippets.rectangular((300, 200), height=150, width=100, depth=10, mirror=True)]
    svg_string = ''.join(svg for svg in svgs)

    filename = 'sample.svg'
    with open(filename, 'w') as f:
        f.write(svg_header + svg_string + svg_footer)


if __name__ == "__main__":
    main()
