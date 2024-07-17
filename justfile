run:
    # manim -pql slides.py
    manim-slides render -ql slides.py Presentation
    manim-slides present Presentation
    
run_prod:
    manim-slides render slides.py Presentation
    manim-slides present Presentation
