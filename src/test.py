from variable_val import VariableVal

from manim import *
from manim_slides import Slide

class TestVariableVal(Slide):
    def construct(self):
        self.variable_val = VariableVal(UP * 3, "x", "", "5")

        self.add(self.variable_val)

        transform_1 = self.variable_val.return_translate_animation(new_lhs_prt2="-3", perform_arithmetic=True)
        self.play(transform_1)

        self.wait()

        print(self.mobjects)

        # self.remove(self.variable_val)

        self.wait()

        self.play(GrowFromCenter(Dot()))

        # transform_2 = self.variable_val.return_translate_animation(new_lhs_prt2="", new_rhs_prt2="+3", perform_arithmetic=False)
        # self.play(transform_2)
        #
        # self.wait()
        #
        # transform_3 = self.variable_val.return_translate_animation(new_rhs_prt1="8", new_rhs_prt2="", perform_arithmetic=True)
        # self.play(transform_3)
        #
        # self.wait()
        #
        # # transform_4 = self.variable_val.return_translate_animation(new_lhs_prt2="+9", new_rhs_prt2="", perform_arithmetic=True)
        # # self.play(transform_4)
        # #
        # # transform_5 = self.variable_val.return_translate_animation(new_lhs_prt2="", new_rhs_prt2="-9", perform_arithmetic=False)
        # # self.play(transform_5)
        #
        # self.wait()
        #
        # transform_6 = self.variable_val.return_translate_animation(new_rhs_prt1="-1", new_rhs_prt2="", perform_arithmetic=True)
        # self.play(transform_6)
        #
        # self.wait()
        #
        # self.play(
        #     *(Circumscribe(current_mobject) for current_mobject in self.variable_val.submobjects[0])
        # )
        #
        # self.wait()
        #
        # transform_7 = self.variable_val.return_translate_animation(new_rhs_prt1="5", perform_arithmetic=True)
        # self.play(transform_7)
