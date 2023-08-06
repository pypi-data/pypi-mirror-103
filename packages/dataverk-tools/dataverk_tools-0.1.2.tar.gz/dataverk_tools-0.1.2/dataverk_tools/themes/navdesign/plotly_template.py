from .colors import *
from .sequential import navBlaGulRod, navRodGulBla
from .nav import *
import plotly.graph_objects as go
import plotly.io as pio

plotly_template = pio.templates["plotly_white"]

plotly_template.layout.colorscale = go.layout.Colorscale(
    diverging=navColors,
    sequential=navBlaGulRod,
    sequentialminus=navRodGulBla
)

plotly_template.layout.font = go.layout.Font(
    color = fontColor,
    family = "'Open Sans', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'"
)

plotly_template.layout.colorway = (navLysBla, navBla, navOransje, navRod, navLilla, navGul, navGronn, navLimeGronn, navDypBla )




