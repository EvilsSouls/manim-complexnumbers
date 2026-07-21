from variable_val import VariableVal

from manim import *
from manim_slides import Slide

class TestVariableVal(Slide):
    def construct(self):
        self.variable_val = VariableVal(UP * 3, "x", "", "5")

        transform_1 = self.variable_val.return_translate_animation(new_lhs_prt2="-3")
        self.play(transform_1)

        transform_2 = self.variable_val.return_translate_animation(new_lhs_prt2="", new_rhs_prt2="+3", custom_transform_target=('L2', 'R2'), combine_rhs=False)
        self.play(transform_2)

        transform_3 = self.variable_val.return_translate_animation(new_rhs_prt1="8", new_rhs_prt2="")
        self.play(transform_3)

        transform_4 = self.variable_val.return_translate_animation(new_lhs_prt2="+9")
        self.play(transform_4)

        transform_5 = self.variable_val.return_translate_animation(new_lhs_prt2="", new_rhs_prt2="-9", custom_transform_target=('L2', 'R2'), combine_rhs=False)
        self.play(transform_5)

        transform_6 = self.variable_val.return_translate_animation(new_rhs_prt1="-1", new_rhs_prt2="")
        self.play(transform_6)

        transform_7 = self.variable_val.return_translate_animation(new_lhs_prt2="-6")
        self.play(transform_7)

        transform_8 = self.variable_val.return_translate_animation(new_lhs_prt2="", new_rhs_prt2="+6", custom_transform_target=('L2', 'R2'), combine_rhs=False)
        self.play(transform_8)

        transform_9 = self.variable_val.return_translate_animation(new_rhs_prt1="5", new_rhs_prt2="")
        self.play(transform_9)

        transform_10 = self.variable_val.return_translate_animation(new_lhs_prt1="x", new_lhs_prt2="^2", new_rhs_prt1="2", new_rhs_prt2="")
        self.play(transform_10)

        transform_11 = self.variable_val.return_translate_animation(new_lhs_prt2="", new_rhs_prt1=r"\sqrt{", new_rhs_prt2=r"2}", custom_transform_target=[('L2', 'R1'), ('R1', 'R2')], combine_rhs=False, new_rhs_prt2_color=WHITE)
        self.play(transform_11)
