from manim import *
from uarr_animations.base import SceneWithMixin
from functools import partial


def data(scene: SceneWithMixin):
    text = partial(Text, font_size=20)
    tex = partial(Tex, font_size=25)
    img_size = 2.5

    derisi_original = ImageMobject("images/derisi_microarray.jpg").scale_to_fit_width(img_size)
    derisi_input = ImageMobject("images/derisi-noise-added.png").scale_to_fit_width(img_size)
    ours_gt = ImageMobject("images/gt_ex0_test.png").scale_to_fit_width(img_size)
    ours_input = ImageMobject("images/input_ex0_test.png").scale_to_fit_width(img_size)

    images = Group(derisi_original, derisi_input, ours_gt, ours_input)
    images.arrange_in_grid(2, 2, buff=1.0)
    images.move_to(ORIGIN)

    derisi_caption = text("DeRisi (real):").next_to(derisi_original, LEFT)
    ours_caption = text("Ours (synthetic):").next_to(ours_gt, LEFT)

    derisi_caption_original = tex(r"$I$ (original image)").next_to(derisi_original, DOWN).shift(0.1 * UP)
    derisi_caption_input = tex(r"$I_\eta$ (noise-added)").next_to(derisi_input, DOWN).shift(0.1 * UP)

    ours_caption_original = tex(r"$G$ (ground-truth image)").next_to(ours_gt, DOWN)
    ours_caption_input = tex(r"$I_\eta$ (noise-added)").next_to(ours_input, DOWN)

    scene.play(
        FadeIn(images),
        FadeIn(derisi_caption_original),
        FadeIn(ours_caption_original),
        FadeIn(derisi_caption_input),
        FadeIn(ours_caption_input),
        FadeIn(derisi_caption),
        FadeIn(ours_caption),
        lag_ratio=0.3
    )
