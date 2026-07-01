from manim import *

class TestScene(Scene):
    def construct(self) -> None:
        test_mobj1 = MathTex("x", r"\hskip 0pt", "=", "3", "+2", font_size=60)
        test_mobj2 = MathTex("x", r"\hskip 0pt", "=", "3", "+2", font_size=60).next_to(test_mobj1, DOWN)

        self.add(test_mobj1, test_mobj2)

        self.wait(1)

        self.play(test_mobj1.animate.set_fill(opacity=0), FadeOut(test_mobj2))

        self.wait(1)
