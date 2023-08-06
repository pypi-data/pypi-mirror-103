from .._swatches import _swatches
from .._colormaps import _linear3color
from . import nav as _nav

def swatches():
    return _swatches(__name__, globals())

swatches.__doc__ = _swatches.__doc__

navBlaGulRod = _linear3color(_nav.navBla, _nav.navGul, _nav.navRod)
navRodGulBla = _linear3color(_nav.navRod, _nav.navGul, _nav.navBla)
navGronnGraBla = _linear3color(_nav.navGronn, _nav.navLysGra, _nav.navBla,9)
navGronnGraOransje = _linear3color(_nav.navGronn, _nav.navLysGra, _nav.navOransje,9)

navBlaHvitRod = _linear3color(_nav.navBla, '#FFFFFF', _nav.navRod)
navRodHvitBla = _linear3color(_nav.navRod, '#FFFFFF', _nav.navBla)
navGronnHvitBla = _linear3color(_nav.navGronn, '#FFFFFF', _nav.navBla)
navGronnHvitOransje = _linear3color(_nav.navGronn, '#FFFFFF', _nav.navOransje)



   
