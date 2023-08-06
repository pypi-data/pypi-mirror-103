from .._swatches import _swatches
from .colors import navColors, navGrays

def swatches():
    return _swatches(__name__, globals())

swatches.__doc__ = _swatches.__doc__






   
