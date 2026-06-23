import numpy as np
from manim import *
from manim_slides import Slide
import MF_Tools as mft

from manim.typing import Vector3DLike
from manim.utils.color import ManimColor

# Consider inheriting from MathTex. Should make it a lot easier to mutate attributes to not just update the mobject but also the values

class VariableVal(MathTex):
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

        self.transform_target: None | VariableVal = None

        # super().__init__("Placeholder String")
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
        super().__init__(self.get_string())
        # self.become(MathTex(self.get_string()))

        # Set colors
        VGroup(self[0].submobjects[slice(*self.get_lhs_prt1_range())]).set_color(self.lhs_prt1_color)
        VGroup(self[0].submobjects[slice(*self.get_lhs_prt2_range())]).set_color(self.lhs_prt2_color)
        VGroup(self[0].submobjects[slice(*self.get_rhs_prt1_range())]).set_color(self.rhs_prt1_color)
        VGroup(self[0].submobjects[slice(*self.get_rhs_prt2_range())]).set_color(self.rhs_prt2_color)

        # Update Position
        equal_sign_glyph = self[0].submobjects[self.get_equal_sign_index()]
        pos_diff = self.tex_location - equal_sign_glyph.get_center()
        self.shift(pos_diff)

    def become_transform_target(self):
        assert self.transform_target is not None, "No transform target found"

        self.tex_location = self.transform_target.tex_location
        self.lhs_prt1 = self.transform_target.lhs_prt1
        self.lhs_prt2 = self.transform_target.lhs_prt2
        self.rhs_prt1 = self.transform_target.rhs_prt1
        self.rhs_prt2 = self.transform_target.rhs_prt2
        self.lhs_prt1_color = self.transform_target.lhs_prt1_color
        self.lhs_prt2_color = self.transform_target.lhs_prt2_color
        self.rhs_prt1_color = self.transform_target.rhs_prt1_color
        self.rhs_prt2_color = self.transform_target.rhs_prt2_color

        self.become(self.transform_target)

        self.transform_target = None

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

        self.transform_target = VariableVal(**kwargs)

        src_lhs_prt1_range = np.arange(*self.get_lhs_prt1_range())
        src_lhs_prt2_range = np.arange(*self.get_lhs_prt2_range())
        src_rhs_prt1_range = np.arange(*self.get_rhs_prt1_range())
        src_rhs_prt2_range = np.arange(*self.get_rhs_prt2_range())

        dest_lhs_prt1_range = np.arange(*self.transform_target.get_lhs_prt1_range())
        dest_lhs_prt2_range = np.arange(*self.transform_target.get_lhs_prt2_range())
        dest_rhs_prt1_range = np.arange(*self.transform_target.get_rhs_prt1_range())
        dest_rhs_prt2_range = np.arange(*self.transform_target.get_rhs_prt2_range())

        # Create Transformation Tuples
        if perform_arithmetic:
            transformation_tuples = [
                (list(src_lhs_prt1_range), list(dest_lhs_prt1_range)),
                (list(src_lhs_prt2_range), list(dest_lhs_prt2_range), {"delay":0.5}),
                ([self.get_equal_sign_index()], [self.transform_target.get_equal_sign_index()]),
                (list(np.concatenate((src_rhs_prt1_range, src_rhs_prt2_range))), list(dest_rhs_prt1_range)),
                # ([], list(dest_lhs_prt2_range)) # Should not really be needed? I am really unsure of myself
            ]
        else:
            transformation_tuples = [
                (list(src_lhs_prt1_range), list(dest_lhs_prt1_range)),
                ([self.get_equal_sign_index()], [self.transform_target.get_equal_sign_index()]),
                (list(src_rhs_prt1_range), list(dest_rhs_prt1_range)),
                (list(src_lhs_prt2_range), list(dest_rhs_prt2_range), {"path_arc": PI}),
                # Add Comment here
            ]

        animation = mft.TransformByGlyphMap(
            self,
            self.transform_target,
            *transformation_tuples,
            introduce_individually=True,
            default_introducer=Write,
            default_transformer=Transform,
            **transform_kwargs,
        )

        # Incredibly hacky monkey patching that overrides the default behavior, which assumes that
        # ReplacementTransform or something similar is used, meaning that mobB should be added to
        # the screen and the initial state of mobA reset
        def patched_clean_up_meth(self, scene):
            # Call the clean up method of AnimationGroup
            super(mft.TransformByGlyphMap, self).clean_up_from_scene(scene)
            scene.remove(self.mobA)

            # Cleanse all remaining orphaned submobjects from introducers
            # You do not comprehend the amounts of debugging I had to do to find
            # this incredibly hacky solution inside an already existing monkey patch
            scene.add(self.mobB)
            scene.remove(self.mobB)

            self.mobA.become_transform_target()

            scene.add(self.mobA)
        animation.clean_up_from_scene = patched_clean_up_meth.__get__(animation)

        return animation

class VariableValTest(Slide):
    def construct(self):
        # variable_val = VariableVal(UP * 3, "x", "", "5", "")
        # # self.play(Write(variable_val), run_time=1)
        # self.add(variable_val)
        #
        # transform_animation_1 = variable_val.return_translate_animation(new_lhs_prt2="+3", perform_arithmetic=True)
        # self.play(transform_animation_1)
        # print(self.mobjects)

        # self.wait(2)
        variable_val = VariableVal(UP * 3, "x", "+3", "5", "")

        transform_animation_2 = variable_val.return_translate_animation(new_lhs_prt2="", new_rhs_prt2="-3", perform_arithmetic=False)
        self.play(transform_animation_2)
        print(self.mobjects)

        # self.wait(2)
        #
        # transform_animation_3 = variable_val.return_translate_animation(new_rhs_prt1="2", new_rhs_prt2="", perform_arithmetic=True)
        # self.play(transform_animation_3)
        # print(self.mobjects)
