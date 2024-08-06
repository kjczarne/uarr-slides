from manim import *
from uarr_animations.microarray import create_microarray
from uarr_animations.wavelet_diff import wavelet_diff
from uarr_animations.maxpool_readout import maxpool
from uarr_animations.eatme import eatme
from uarr_animations.data import data
from uarr_animations.base import SceneWithMixin


class Microarray(SceneWithMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__post_init__()

    def construct(self):
        create_microarray(self, logo=True)
        # maxpool(self)
        # wavelet_diff(self)
        # eatme(self)
        # data(self)
