from .colors import *
from .scales import *

fontFamily = "'Open Sans', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'"



def altair_template():
    # Typography
    font = fontFamily
    labelFont = fontFamily 
    sourceFont = fontFamily
    # Colors
    main_palette = discrete
    sequential_palette = sequential
    return {
        "width": 685,
        "height": 450,
        "config": {
            "title": {
                "font": font,
                "fontColor": fontColor
            },
            "axisX": {
                "domainColor": axisColor,
                "tickColor": axisColor,
            },
            "axisY": {
                "gridColor": gridColor,
            },
            "range": {
                "category": discrete,
                "diverging": diverging
            },
            "legend": {
                "labelFont": labelFont,
                "title": "", # set it to no-title by default
            },
            "view": {
                "stroke": "transparent", 
            },
            "area": {
               "fill": markColor,
           },
           "line": {
               "color": markColor,
               "stroke": markColor,
           },
           "trail": {
               "color": markColor,
               "stroke": markColor,
           },
           "path": {
               "stroke": markColor,
               "strokeWidth": 0.5,
           },
           "point": {
               "filled": True,
           },
           "text": {
               "font": sourceFont,
               "color": markColor
           }
        }
    }