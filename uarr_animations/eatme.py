from manim import *
import numpy as np
from uarr_animations.base import SceneWithMixin

arr_h, arr_w = 3, 3
pixels_perr_arr_edge = 3

def e_upsampled(scene: SceneWithMixin):
    arr_pixel_h, arr_pixel_w = arr_h * pixels_perr_arr_edge, arr_w * pixels_perr_arr_edge
    e_gt = np.round(np.random.rand(int(arr_h * arr_w)), 2)
    e_gt_mob = Matrix([e_gt]).to_edge(UP)
    scene.add(e_gt_mob)
    elements = e_gt_mob.get_elements()
    offset = 1.5
    create_runtime = 0.3
    fade_out_runtime = 0.4
    for e_ in elements:
        e = e_.copy()
        scene.play(Indicate(e_))
        scene.play(e.animate.move_to(ORIGIN))
        scene.wait(0.3)
        copies = [e.copy() for _ in range(pixels_perr_arr_edge ** 2 - 1)]
        copies[0].move_to(e.get_center() + offset * UP + offset * LEFT)
        copies[1].move_to(e.get_center() + offset * UP)
        copies[2].move_to(e.get_center() + offset * UP + offset * RIGHT)
        copies[3].move_to(e.get_center() + offset * LEFT)
        copies[4].move_to(e.get_center() + offset * RIGHT)
        copies[5].move_to(e.get_center() + offset * DOWN + offset * LEFT)
        copies[6].move_to(e.get_center() + offset * DOWN)
        copies[7].move_to(e.get_center() + offset * DOWN + offset * RIGHT)
        scene.play(*[Create(c, run_time=create_runtime) for c in copies])
        scene.play(*[FadeOut(c, run_time=fade_out_runtime) for c in copies],
                   FadeOut(e, run_time=fade_out_runtime))
        scene.wait(0.1)
    scene.play(FadeOut(e_gt_mob))
    e_gt_reshaped = e_gt.reshape(arr_h, arr_w)
    e_gt_mob_reshaped = Matrix(e_gt_reshaped).to_edge(LEFT)
    hsv_base_color = (0.6, 1, 1)
    # colors_reshaped = [(hsv_base_color[0], hsv_base_color[1], np.random.uniform(0.2, 1))
    #                    for _ in range(arr_h * arr_w)]
    colors_reshaped = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, PINK, TEAL, MAROON]
    colors_reshaped_2 = np.array([RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, PINK, TEAL, MAROON]).reshape(arr_h, arr_w)
    for idx, element in enumerate(e_gt_mob_reshaped.get_elements()):
        element.set_color(colors_reshaped[idx])
    e_gt_upsampled = np.kron(e_gt_reshaped, np.ones((pixels_perr_arr_edge, pixels_perr_arr_edge)))
    e_gt_mob_upsampled = Matrix(e_gt_upsampled).scale(0.5).to_edge(RIGHT)
    colors_upsampled = np.kron(colors_reshaped_2, np.full((pixels_perr_arr_edge, pixels_perr_arr_edge), WHITE))
    colors_upsampled = colors_upsampled.flatten()
    for idx, element in enumerate(e_gt_mob_upsampled.get_elements()):
        element.set_color(colors_upsampled[idx])
    arrow = LabeledArrow(label=r"\mathrm{resize}", start=e_gt_mob_reshaped.get_right(), end=e_gt_mob_upsampled.get_left())
    creation_anim = DrawBorderThenFill
    scene.play(creation_anim(e_gt_mob_reshaped))
    scene.wait(0.5)
    scene.play(creation_anim(arrow, lag_ratio=0.5))
    scene.wait(0.5)
    scene.play(creation_anim(e_gt_mob_upsampled))
    scene.wait(2)
    return e_gt_mob_reshaped, e_gt_mob_upsampled, arrow, e_gt_upsampled, colors_upsampled


def eatme(scene: SceneWithMixin):
    e_gt_mob_reshaped, e_gt_mob_upsampled, arrow, e_gt_upsampled, colors_upsampled = e_upsampled(scene)
    scene.play(FadeOut(e_gt_mob_reshaped), FadeOut(arrow))
    scene.play(e_gt_mob_upsampled.animate.move_to(ORIGIN))
    scene.play(e_gt_mob_upsampled.animate.shift(LEFT))

    # Create a Weight Matrix:
    ast_text = Tex(r"$\ast$").next_to(e_gt_mob_upsampled, RIGHT) 
    w_text = Text("W").next_to(ast_text, RIGHT)
    scene.play(Write(ast_text), Write(w_text))

    W = np.round(np.random.rand(arr_h * pixels_perr_arr_edge, arr_w * pixels_perr_arr_edge), 2)

    scene.play(e_gt_mob_upsampled.animate.to_edge(LEFT))
    scene.play(ast_text.animate.next_to(e_gt_mob_upsampled))
    W_mob = Matrix(W)
    W_mob = W_mob.scale(0.5).next_to(ast_text, RIGHT)
    scene.play(Transform(w_text, W_mob))
    scene.add(W_mob)
    scene.remove(w_text)

    prod = np.round(e_gt_upsampled * W, 2)
    prod_mob = Matrix(prod)
    scene.play(FadeOut(e_gt_mob_upsampled), FadeOut(ast_text))
    scene.play(W_mob.animate.move_to(ORIGIN))
    scene.play(Transform(W_mob, prod_mob))
    for idx, element in enumerate(prod_mob.get_elements()):
        scene.play(element.animate.set_color(colors_upsampled[idx]), run_time=0.05)
    scene.wait(2)
    scene.remove(W_mob)

    # Transform the big matrix into a square
    square = Square(side_length=4, color=ORANGE).set_fill(ORANGE, 1).set_stroke(WHITE, 2)
    scene.play(Transform(prod_mob, square))
    scene.add(square)
    scene.remove(prod_mob)

    # Caption the square:
    caption_w = Tex(r"$E_{\mathrm{upsampled}} \ast W$", font_size=40).next_to(square, DOWN)
    scene.play(Write(caption_w))

    # Move these to the left:
    scene.play(square.animate.to_edge(LEFT), caption_w.animate.to_edge(LEFT))

    # Indicate elementwise product between feature maps and the weighted expression values:
    ast2 = Tex(r"$\ast$").next_to(square, RIGHT)
    scene.play(Write(ast2))

    # Visualize feature maps as overlapping squares:
    feature_maps = []
    for i in range(3):
        feature_map = Square(side_length=4, color=BLUE).set_fill(BLUE, 1).set_stroke(WHITE, 2).next_to(ast2, RIGHT)
        feature_map.shift(i * 0.3 * RIGHT)
        feature_map.shift(i * 0.3 * DOWN)
        feature_maps.append(feature_map)
    feature_maps_copy = [fm.copy() for fm in feature_maps]
    fm_caption = Tex(r"$O_{\xi}$").next_to(feature_maps[-1], DOWN)
    fm_caption_copy = fm_caption.copy()
    scene.play(*[Create(fm) for fm in feature_maps], Write(fm_caption))

    # Leave only the feature maps in view and change their color:
    scene.play(FadeOut(caption_w), FadeOut(square), FadeOut(ast2), FadeOut(fm_caption))
    scene.remove(square)
    scene.wait(1)

    # Sigmoid over the feature maps:
    font_size_brackets = 300
    operator_font_size = 60
    lbr = Tex(r"(", font_size=font_size_brackets).next_to(feature_maps[0].get_left(), LEFT)
    sigmoid = Tex(r"$\sigma$", font_size=operator_font_size).next_to(lbr, LEFT)
    rbr = Tex(r")", font_size=font_size_brackets).next_to(feature_maps[-1].get_right(), RIGHT).shift(0.6 * UP)
    post_caption = Tex(r"$\sigma(E_{\mathrm{upsampled}} \ast W \ast O_{\xi})$").next_to(feature_maps[0], DOWN).shift(0.5 * DOWN)
    scene.play(Write(sigmoid))
    scene.play(Write(lbr), Write(rbr))
    scene.wait(2)
    scene.play(*[fm.animate.set_color(RED) for fm in feature_maps],
                FadeOut(sigmoid),
                FadeOut(lbr),
                FadeOut(rbr),
                Write(post_caption))
    scene.wait(2)

    fm_copy_animations = []
    for idx, fm in enumerate(feature_maps_copy):
        if idx == 0:
            fm.to_edge(LEFT)
        else:
            fm.to_edge(LEFT).shift(idx * 0.3 * RIGHT)
        fm_copy_animations.append(FadeIn(fm))

    offset_from_center = 1.1
    for fm in feature_maps:
        fm_copy_animations.append(fm.animate.shift(offset_from_center * RIGHT))
    fm_copy_animations.append(post_caption.animate.shift(offset_from_center * RIGHT))
    
    ast_fm = Tex(r"$\ast$").next_to(feature_maps_copy[-1], RIGHT)
    fm_caption_copy = fm_caption_copy.next_to(feature_maps_copy[-1], DOWN)
    scene.play(*fm_copy_animations, Write(ast_fm), Write(fm_caption_copy))

    scene.wait(2)

    fadeout_animations = []
    for fm in feature_maps_copy:
        fadeout_animations.append(FadeOut(fm))
    for fm in feature_maps:
        # recover original position
        fadeout_animations.append(fm.animate.shift(offset_from_center * LEFT))
    fadeout_animations.extend([FadeOut(fm_caption_copy), FadeOut(ast_fm),
                               post_caption.animate.shift(offset_from_center * LEFT),
                               FadeOut(post_caption)])
    scene.play(*fadeout_animations)

    # Feed to the output layer:

    lbr = Tex(r"(", font_size=font_size_brackets).next_to(feature_maps[0].get_left(), LEFT)
    out = Tex(r"$\mathrm{out}$", font_size=operator_font_size).next_to(lbr, LEFT)
    rbr = Tex(r")", font_size=font_size_brackets).next_to(feature_maps[-1].get_right(), RIGHT).shift(0.6 * UP)
    scene.play(Write(out))
    scene.play(Write(lbr), Write(rbr))
    out_img = Square(side_length=4, color=GREEN).set_fill(GREEN, 1).set_stroke(WHITE, 2)
    out_img_caption = Tex(r"$O$").next_to(out_img, DOWN)
    scene.play(*[FadeOut(fm) for fm in feature_maps],
               FadeOut(out),
               FadeOut(lbr),
               FadeOut(rbr))
    scene.play(Create(out_img),
               Write(out_img_caption))
    scene.wait(2)
