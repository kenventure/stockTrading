from collections import OrderedDict
import numpy as np

from bokeh.plotting import *
from bokeh.models import HoverTool

x = np.linspace(0, 4*np.pi, 200)
y = np.sin(x)

output_file("line_dots.html", title="line.py example")

source = ColumnDataSource(
    data=dict(
        x=x,
        y=y,
        label=["%s X %s" % (x_, y_) for x_, y_ in zip(x, y)]
    )
)
TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset,hover,previewsave"
p = figure(title="simple line example", tools=TOOLS)
p.line('x', 'y', color="#2222aa", line_width=2, source=source)
p.circle('x', 'y', color="#2222aa", line_width=2, source=source)

hover =p.select(dict(type=HoverTool))
hover.tooltips = OrderedDict([
    ("index", "$index"),
    ("(xx,yy)", "(@x, @y)"),
    ("label", "@label"),
])

show(p)