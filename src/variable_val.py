import numpy as np
from manim import *
import MF_Tools as mft

from manim.typing import Vector3DLike
from manim.utils.color import ManimColor

class VariableVal():
    def __init__(
        self,
        tex_location: Vector3DLike,
        lhs_prt1="x",
        lhs_prt2="",
        rhs_prt1="",
        rhs_prt2="",
        lhs_prt1_color=WHITE,
        lhs_prt2_color=WHITE,
        rhs_prt1_color=WHITE,
        rhs_prt2_color=RED,
    ):
        self.tex_location = tex_location

        self.lhs_prt1 = lhs_prt1
        self.lhs_prt2 = lhs_prt2
        self.rhs_prt1 = rhs_prt1
        self.rhs_prt2 = rhs_prt2

        self.lhs_prt1_color = lhs_prt1_color
        self.lhs_prt2_color = lhs_prt2_color
        self.rhs_prt1_color = rhs_prt1_color
        self.rhs_prt2_color = rhs_prt2_color

        self.update_mobject()

    def get_string(self) -> str:
        return self.lhs_prt1 + self.lhs_prt2 + "=" + self.rhs_prt1 + self.rhs_prt2

    def get_lhs_prt1_range(self) -> tuple[int, int]:
        return (0, len(self.lhs_prt1))

    def get_lhs_prt2_range(self) -> tuple[int, int]:
        start_index = len(self.lhs_prt1)
        return (start_index, start_index + len(self.lhs_prt2))

    def get_rhs_prt1_range(self) -> tuple[int, int]:
        # Must add one due to equal sign
        start_index = len(self.lhs_prt1) + len(self.lhs_prt2) + 1
        return (start_index, start_index + len(self.rhs_prt1))

    def get_rhs_prt2_range(self) -> tuple[int, int]:
        # Once again have to add one due to the equal sign
        start_index = len(self.lhs_prt1) + len(self.lhs_prt2) + len(self.rhs_prt1) + 1
        return (start_index, start_index + len(self.rhs_prt2))

    def get_equal_sign_index(self) -> int:
        # print(f"equal_ind: {len(self.lhs_prt1) + len(self.lhs_prt2)}")
        return len(self.lhs_prt1) + len(self.lhs_prt2)

    def update_mobject(self) -> None:
        # print(f"string: {self.get_string()}")
        self.mobject = MathTex(self.get_string())

        # Set colors
        VGroup(self.mobject[0].submobjects[slice(*self.get_lhs_prt1_range())]).set_color(self.lhs_prt1_color)
        VGroup(self.mobject[0].submobjects[slice(*self.get_lhs_prt2_range())]).set_color(self.lhs_prt2_color)
        VGroup(self.mobject[0].submobjects[slice(*self.get_rhs_prt1_range())]).set_color(self.rhs_prt1_color)
        VGroup(self.mobject[0].submobjects[slice(*self.get_rhs_prt2_range())]).set_color(self.rhs_prt2_color)

        # Update Position
        equal_sign_glyph = self.mobject[0].submobjects[self.get_equal_sign_index()]
        pos_diff = self.tex_location - equal_sign_glyph.get_center()
        self.mobject.shift(pos_diff)

    """
    Any arguments left empty will default to the value of self

    If perform_arithmetic is true lhs will be transformed into itself and rhs will be combined
    else if perform_arithmetic is false, lhs_prt2 will be transformed into lhs_prt1 and the rest will stay the same
    """
    def return_translate_animation(
        self,
        new_tex_location: Vector3DLike | None = None,
        new_lhs_prt1: str | None = None,
        new_lhs_prt2: str | None = None,
        new_rhs_prt1: str | None = None,
        new_rhs_prt2: str | None = None,
        new_lhs_prt1_color: ManimColor | None = None,
        new_lhs_prt2_color: ManimColor | None = None,
        new_rhs_prt1_color: ManimColor | None = None,
        new_rhs_prt2_color: ManimColor | None = None,
        *,
        perform_arithmetic,
        **transform_kwargs,
    ) -> mft.TransformByGlyphMap:

        kwargs = {}

        kwargs["tex_location"] = self.tex_location if new_tex_location is None else new_tex_location
        kwargs["lhs_prt1"] = self.lhs_prt1 if new_lhs_prt1 is None else new_lhs_prt1
        kwargs["lhs_prt2"] = self.lhs_prt2 if new_lhs_prt2 is None else new_lhs_prt2
        kwargs["rhs_prt1"] = self.rhs_prt1 if new_rhs_prt1 is None else new_rhs_prt1
        kwargs["rhs_prt2"] = self.rhs_prt2 if new_rhs_prt2 is None else new_rhs_prt2
        kwargs["lhs_prt1_color"] = self.lhs_prt1_color if new_lhs_prt1_color is None else new_lhs_prt1_color
        kwargs["lhs_prt2_color"] = self.lhs_prt2_color if new_lhs_prt2_color is None else new_lhs_prt2_color
        kwargs["rhs_prt1_color"] = self.rhs_prt1_color if new_rhs_prt1_color is None else new_rhs_prt1_color
        kwargs["rhs_prt2_color"] = self.rhs_prt2_color if new_rhs_prt2_color is None else new_rhs_prt2_color

        self.transform_object = VariableVal(**kwargs)

        src_lhs_prt1_range = np.arange(*self.get_lhs_prt1_range())
        src_lhs_prt2_range = np.arange(*self.get_lhs_prt2_range())
        src_rhs_prt1_range = np.arange(*self.get_rhs_prt1_range())
        src_rhs_prt2_range = np.arange(*self.get_rhs_prt2_range())

        dest_lhs_prt1_range = np.arange(*self.transform_object.get_lhs_prt1_range())
        dest_lhs_prt2_range = np.arange(*self.transform_object.get_lhs_prt2_range())
        dest_rhs_prt1_range = np.arange(*self.transform_object.get_rhs_prt1_range())
        dest_rhs_prt2_range = np.arange(*self.transform_object.get_rhs_prt2_range())

        # print(f"Perform Arithmetic: {perform_arithmetic}")
        # print(f"src_l1: {src_lhs_prt1_range} \n src_l2: {src_lhs_prt2_range} \n src_r1: {src_rhs_prt1_range} \n src_r2: {src_rhs_prt2_range} \n\n")
        # print(f"dest_l1: {dest_lhs_prt1_range} \n dest_l2: {dest_lhs_prt2_range} \n dest_r1: {dest_rhs_prt1_range} \n dest_r2: {dest_rhs_prt2_range} \n\n")
        # print("----------------\n\n\n")

        # Create Transformation Tuples
        if perform_arithmetic:
            transformation_tuples = [
                (list(src_lhs_prt1_range), list(dest_lhs_prt1_range)),
                (list(src_lhs_prt2_range), list(dest_lhs_prt2_range), {"delay": 0.5}),
                ([self.get_equal_sign_index()], [self.transform_object.get_equal_sign_index()]),
                (list(np.concatenate((src_rhs_prt1_range, src_rhs_prt2_range))), list(dest_rhs_prt1_range)),
                # ([], list(dest_lhs_prt2_range)) # Should not really be needed? I am really unsure of myself
            ]
        else:
            transformation_tuples = [
                (list(src_lhs_prt1_range), list(dest_lhs_prt1_range)),
                ([self.get_equal_sign_index()], [self.transform_object.get_equal_sign_index()]),
                (list(src_rhs_prt1_range), list(dest_rhs_prt1_range)),
                (list(src_lhs_prt2_range), list(dest_rhs_prt2_range), {"path_arc": PI/2}),
                # (list(src_rhs_prt2_range), []) # Should also probably not be needed
            ]

        # print(transformation_tuples)
        animation = mft.TransformByGlyphMap(
            self.mobject,
            self.transform_object.mobject,
            *transformation_tuples,
            introduce_individually=True,
            default_introducer=Write,
            default_transformer=ReplacementTransform,
            **transform_kwargs,
        )

        return animation

