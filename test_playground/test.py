from manim import *

class TestScene(Scene):
    def construct(self) -> None:
        test_mobj = MathTex("x", r"\hskip 0pt", "=", "3", "+2", font_size=100)

        self.add(test_mobj)

        print("debug msg: ", test_mobj[1].submobjects)
