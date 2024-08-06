run OUTPUT_FILENAME FORMAT="mp4" QUALITY="l":
    manim render -pq{{QUALITY}} --format {{FORMAT}} -o {{OUTPUT_FILENAME}} uarr_animations/main.py

slides_run QUALITY="l":
    manim-slides render -q{{QUALITY}} uarr_animations/slides.py Presentation
    manim-slides present Presentation
