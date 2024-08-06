from manim import *
from uarr_animations.base import SceneMixin

def wavelet_diff(scene: SceneMixin | Scene):
    t1 = scene.text("input")
    t2 = scene.text("output")
    input_img = ImageMobject("images/uarr-wavelet-input.png")
    output_img = ImageMobject("images/uarr-wavelet-output.png")
    t1.next_to(input_img, UP)
    t2.next_to(output_img, UP)
    scene.add(t1)
    img_transition = Transform(input_img, output_img)
    text_transition = Transform(t1, t2)
    scene.play(AnimationGroup(img_transition, text_transition), run_time=2)
