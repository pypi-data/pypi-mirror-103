import plotly.graph_objects as go
import plotly.io as pio
import base64

# with open("/home/jovyan/Rød.png", "rb") as image_file:
#     encoded_string = base64.b64encode(image_file.read()).decode()
# #add the prefix that plotly will want when using the string as source
# encoded_image = "data:image/png;base64," + encoded_string

plotly_template = pio.templates["none"]

plotly_template.layout.images = [go.layout.Image(
                                                dict(
                                                source="https://www.nav.no/_/asset/no.nav.navno:1585254115/img/navno/logo.svg",
                                                xref="paper", yref="paper",
                                                x=1.1, y=1.13,
                                                sizex=0.18, sizey=0.18,
                                                xanchor="right", yanchor="bottom",
                                                name='logo'
                                                ))]
plotly_template.layout.annotations = [go.layout.Annotation({
                'text': "NB! Dette plottet er ikke offisiell statistikk og må ikke deles utenfor NAV.",
                'font': {
                        'size': 13,
                        'color': 'rgb(116, 101, 130)',
                        },
                'showarrow': False,
                'align': 'center',
                'x': 0.5,
                'y': 1.1,
                'xref': 'paper',
                'yref': 'paper',
                'name': 'disclaimer'
                })]

plotly_template.layout.font = go.layout.Font({
            'family' : "Source Sans Pro Semibold",
            'size' : 14,
            'color' : "#3E3832"})