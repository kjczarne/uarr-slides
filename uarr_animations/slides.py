import numpy as np
from manim import *
from manim_slides import Slide
from dataclasses import dataclass, asdict, field
import networkx as nx


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


class StyledSlide(Slide):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__style = None

    @property
    def style(self) -> Styles:
        if self.__style is None:
            self.__style = Styles(
                text=TextStyles()
            )
        return self.__style
    
    def slide_template(self, this_slide_fn):
        objects = this_slide_fn()
        self.next_slide()
        self.wipe(Group(*objects))

    def play_and_wait(self, *args, wait: int = 1, **kwargs):
        self.play(*args, **kwargs)
        self.wait(wait)

    def slide_title(self, text: str, **kwargs):
        return Text(text, **asdict(self.style.text.slide_title)).to_edge(UP, buff=0.5)

    def text(self, text: str, **kwargs):
        return Text(text, **asdict(self.style.text.normal), **kwargs)


class Presentation(StyledSlide):

    def title_slide(self):

        # Obligatory logos:
        uw_logo = ImageMobject("images/uw-logo-2.png").scale(0.5).to_edge(UL, buff=0.5)
        vip_logo = ImageMobject("images/viplogo-2.png").scale(0.5).to_edge(UR, buff=0.5)

        # Title and subtitle:
        title = Text("Microarray Image Denoising", **asdict(self.style.text.title)).shift(UP * 1.5)
        subtitle = Paragraph("Leveraging Autoencoders",
                      "and Attention-Based Architectures",
                      "with Synthetic Training Data",
                      **asdict(self.style.text.subtitle),
                      t2c={"Autoencoders": BLUE,
                           "Attention-Based Architectures": BLUE,
                           "Synthetic Training Data": BLUE},
                    #   t2w={"Autoencoders": "BOLD", "Attention-Based Architectures": "BOLD", "Synthetic Training Data": "BOLD"},
                      should_center=True,
                      alignment="center").next_to(title, DOWN, buff=0.5)
        author = Text("Chris Czarnecki", font_size=30).next_to(subtitle, DOWN, buff=0.5)

        self.add(uw_logo)
        self.add(vip_logo)
        self.play(Create(title), run_time=0.5)
        self.play(Create(subtitle), run_time=1)
        self.play_and_wait(Create(author), run_time=0.5, wait=2)
        return title, subtitle, author
        # If you want to clear the logos off the slides after the first slide:
        # return uw_logo, vip_logo, title, subtitle, author

    def what_are_microarrays(self):
        t = self.slide_title("What are microarrays?")
        t2 = self.text("Microarrays are used to study gene expression quantitatively").next_to(t, DOWN, buff=0.5)
        t3 = self.text("...or really any biological process that involves DNA or RNA").next_to(t2, DOWN, buff=0.5)
        microarray = ImageMobject("images/microarray_example.svg.png").scale(2.0).next_to(t3, DOWN, buff=0.5)
        self.play_and_wait(Create(t), run_time=0.5, wait=1)
        self.play_and_wait(Create(t2), run_time=0.5, wait=1)
        self.play_and_wait(Create(t3), run_time=0.5, wait=1)
        self.play_and_wait(FadeIn(microarray), run_time=0.5, wait=2)
        return t, t2, t3, microarray

    def problem_statement(self):
        t = self.slide_title("The Problem")
        t2 = self.text("Microarray images are noisy").next_to(t, DOWN, buff=0.5)
        # BulletedList styling doesn't work in the ctor https://github.com/ManimCommunity/manim/issues/3843
        derisi_microarray = ImageMobject("images/derisi_microarray.jpg")\
            .scale(0.75)\
            .next_to(t2, DOWN, buff=0.5)
        self.play_and_wait(Create(t), run_time=0.5, wait=1)
        self.play_and_wait(Create(t2), run_time=0.5, wait=1)
        self.play_and_wait(FadeIn(derisi_microarray), run_time=0.5, wait=2)
        return t, t2, derisi_microarray

    def problem_statement_2(self):
        t = self.slide_title("The Problem")
        t3 = BulletedList(
            "Low Signal-to-Noise Ratio (SNR)",
            "Low contrast",
            "Low resolution",
            "Artifacts from slide preparation",
            "Artifacts from the scanning process")\
                .set_color(BLACK)
                # .next_to(t, DOWN, buff=0.5)
        self.play_and_wait(Create(t), run_time=0.5, wait=1)
        self.play_and_wait(Create(t3), run_time=0.5, wait=2)
        return t, t3

    def general_image_denoising_methods(self):
        t = self.slide_title("General Image Denoising Methods")
        t2 = self.text("Traditional image processing techniques")\
            .next_to(t, DOWN, buff=0.5)
        t3 = self.text("Deep Learning techniques")\
            .next_to(t2, DOWN, buff=0.5)
        self.play_and_wait(Create(t), run_time=0.5, wait=1)
        self.play_and_wait(Create(t2), run_time=0.5, wait=1)
        self.play_and_wait(Create(t3), run_time=0.5, wait=2)
        return t, t2, t3

    def prior_works(self):
        t = self.slide_title("Prior Works")
        t2 = self.text("Prior works have used traditional image processing techniques...")\
            .next_to(t, DOWN, buff=0.5)
        t3 = self.text("...until 2020")\
            .next_to(t2, DOWN, buff=0.5)
        self.play_and_wait(Create(t), run_time=0.5, wait=1)
        self.play_and_wait(Create(t2), run_time=0.5, wait=1)
        self.play_and_wait(Create(t3), run_time=0.5, wait=2)
        return t, t2, t3

    def prior_works_2(self):
        t = self.slide_title("Denoising Autoencoders")
        ae_diagram = ImageMobject("images/uarr-autoencoder.drawio.png")\
            .scale(1.25)\
            .next_to(t, DOWN, buff=0.5)
        t2 = self.text("Denoising Autoencoders are simple U-Nets trained for the denoising task")\
            .next_to(ae_diagram, DOWN, buff=0.5)
        G = nx.Graph()
        G.add_node("Input")
        G.add_node("Encoder")
        G.add_node("Latent Space")
        G.add_node("Decoder")
        G.add_node("Output")
        G.add_edges_from([("Input", "Encoder"), ("Encoder", "Latent Space"), ("Latent Space", "Decoder"), ("Decoder", "Output")])
        # nodes = VGroup(*[Text(node, color=BLACK) for node in G.nodes])
        # edges = VGroup(*[Line(pos[u], pos[v], color=BLACK) for u, v in G.edges])
        nodes = list(G.nodes)
        edges = list(G.edges)
        mG = Graph(nodes, edges, layout="circular", labels=True)
        mG.set_colors_by_node([BLUE, GREEN, YELLOW, RED, PURPLE])
        self.play_and_wait(Create(t), run_time=0.5, wait=1)
        # self.play_and_wait(FadeIn(ae_diagram), run_time=0.5, wait=1)
        self.play_and_wait(Create(mG), run_time=0.5, wait=1)
        self.play_and_wait(Create(t2), run_time=0.5, wait=2)
        # TODO: If I have enough time I could turn these architecture diagrams into animations
        return t, ae_diagram, t2

    def the_problem_with_prior_works(self):
        t = self.slide_title("The Problem with current SOTA", t2s={"et al.": ITALIC})
        t2 = self.text("Training on real data").next_to(t, DOWN, buff=0.5)
        t3 = self.text("=").next_to(t2, DOWN, buff=0.5)
        t4 = self.text("Training on naturally-noisy data").next_to(t3, DOWN, buff=0.5)
        self.play_and_wait(Create(t), run_time=0.5, wait=1)
        self.play(Create(t2), run_time=0.5)
        self.play(Create(t3), run_time=0.5)
        self.play_and_wait(Create(t4), run_time=0.5, wait=2)
        return t, t2, t3, t4

    def the_idea(self):
        t = self.slide_title("The Idea")
        t2 = self.text("The microarray images are quite regular and simple").next_to(t, DOWN, buff=0.5)
        t3 = self.text("What if we generate synthetic data to train our models?").next_to(t2, DOWN, buff=0.5)
        self.play_and_wait(Create(t), run_time=0.5, wait=1)
        self.play_and_wait(Create(t2), run_time=0.5, wait=1)
        self.play_and_wait(Create(t3), run_time=0.5, wait=2)
        return t, t2, t3

    def synthetic_data_generation(self):
        t = self.slide_title("Synthetic Data Generation")
        microarray = Square(side_length=4, color=BLACK)\
            .set_fill(BLACK, 1)
            # .next_to(t, DOWN, buff=0.5)
        dots = VGroup(*[Dot() for _ in range(16)])\
            .arrange_in_grid(4, 4, buff=0.5)
        self.play_and_wait(Create(t), run_time=0.5, wait=1)
        self.play_and_wait(Create(microarray), run_time=0.5, wait=1)
        self.play(Create(dots), run_time=0.5)
        # Modulate dot intensities:
        hsv_white = (0, 0, 1)
        for dot in dots:
            hue, saturation, value = hsv_white
            value *= np.random.uniform(0.2, 1)
            self.play(dot.animate.set_color(ManimColor.from_hsv((hue, saturation, value))), run_time=0.1)
        return t, microarray, dots

    def construct(self):
        self.camera.background_color = "#f0f0f0"
        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage{enumitem,xcolor}")

        Text.set_default(color=BLACK)
        Tex.set_default(color=BLACK)
        BulletedList.set_default(color=BLACK, fill_color=BLACK, stroke_color=BLACK, tex_template=tex_template)

        slides = [
            # self.title_slide,
            # self.what_are_microarrays,
            # self.problem_statement,
            # self.problem_statement_2,
            # self.prior_works,
            self.prior_works_2,
            # self.the_problem_with_prior_works,
            # self.the_idea,
            # self.synthetic_data_generation
        ]
        for slide in slides:
            self.slide_template(slide)
