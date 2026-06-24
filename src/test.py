from variable_val import VariableVal

from manim import *
from manim_slides import Slide

class TestVariableVal(Slide):
    def construct(self):
        self.variable_val = VariableVal(UP * 3, "x", "", "5")
        transform_1 = self.variable_val.return_translate_animation(new_lhs_prt2="-3", perform_arithmetic=True)
        self.play(transform_1)

        transform_2 = self.variable_val.return_translate_animation(new_lhs_prt2="", new_rhs_prt2="+3", perform_arithmetic=False)
        self.play(transform_2)

        transform_3 = self.variable_val.return_translate_animation(new_rhs_prt1="8", new_rhs_prt2="", perform_arithmetic=True)
        self.play(transform_3)

        self.play(
            *(Circumscribe(current_mobject) for current_mobject in self.variable_val.submobjects[0])
        )

        transform_4 = self.variable_val.return_translate_animation(new_lhs_prt2="+9", new_rhs_prt2="", perform_arithmetic=True)
        self.play(transform_4)

        transform_5 = self.variable_val.return_translate_animation(new_lhs_prt2="", new_rhs_prt2="-9", perform_arithmetic=False)
        self.play(transform_5)
