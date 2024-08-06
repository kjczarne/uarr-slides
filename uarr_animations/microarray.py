from manim import *


def create_microarray(scene: Scene, logo: bool = False):
    microarray = Square(side_length=4, color=BLACK)\
        .set_fill(BLACK, 1)
        # .next_to(t, DOWN, buff=0.5)
    dots = VGroup(*[Dot() for _ in range(16)])\
        .arrange_in_grid(4, 4, buff=0.5)
    scene.play_and_wait(Create(microarray), run_time=0.5, wait=1)
    scene.play(Create(dots), run_time=0.5)
    # Modulate dot intensities:
    hsv_white = (0, 0, 1)
    for dot in dots:
        hue, saturation, value = hsv_white
        value *= np.random.uniform(0.2, 1)
        scene.play(dot.animate.set_color(ManimColor.from_hsv((hue, saturation, value))), run_time=0.1)
