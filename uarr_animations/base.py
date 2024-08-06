from manim import *
from dataclasses import dataclass, field, asdict


@dataclass(frozen=True)
class TextStyle:
    color: ManimColor = field(default_factory=lambda: BLACK)
    font_size: int = 25
    weight: str = "NORMAL"
    slant: str = "NORMAL"


@dataclass(frozen=True)
class TextStyles:
    title: TextStyle = TextStyle(color=ORANGE, font_size=50, weight="BOLD")
    subtitle: TextStyle = TextStyle(font_size=40, weight="BOLD")
    slide_title: TextStyle = TextStyle(font_size=50)
    normal: TextStyle = TextStyle(font_size=25)


@dataclass(frozen=True)
class Styles:
    text: TextStyles


class SceneMixin:
    def play_and_wait(self, *args, wait: int = 1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def __post_init__(self):
        if hasattr(super(), "__post_init__"):
            super().__post_init__()
        # self.camera.background_color = "#f0f0f0"
        self.__style = None

    @property
    def style(self) -> Styles:
        if self.__style is None:
            self.__style = Styles(
                text=TextStyles()
            )
        return self.__style

    def text(self, text: str, **kwargs):
        return Text(text, **asdict(self.style.text.normal), **kwargs)


class SceneWithMixin(Scene, SceneMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__post_init__()

    def construct(self):
        raise NotImplementedError("This method must be implemented in the subclass.")
