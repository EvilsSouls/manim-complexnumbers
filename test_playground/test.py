from manim import *

from variable_val import VariableVal

class TestScene(Scene):
    def construct(self) -> None:
        tex = MathTex(r"\sqrt{", r"2}")

        self.add(tex)

        self.play(Indicate(tex[0]))
        self.play(Indicate(tex[1]))
