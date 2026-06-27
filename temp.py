import numpy as np
from manim import *
from manim_slides import Slide
import MF_Tools as mft

from manim.typing import Vector3DLike
from manim.utils.color import ManimColor

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

        self.update_mobject()

    def get_string(self) -> str:
        return self.lhs_prt1 + self.lhs_prt2 + "=" + self.rhs_prt1 + self.rhs_prt2

    # Incredibly Inefficient
    # TODO: Perhaps change this entire class to not use MF-Tools and instead use the MathTex parts and
    # some custom logic to automatically use Introducer or Remover or Translate
    def get_lhs_prt1_len(self) -> int:
        return len(MathTex(self.lhs_prt1).submobjects[0]) if self.lhs_prt1 else 0

    def get_lhs_prt2_len(self) -> int:
        return len(MathTex(self.lhs_prt2).submobjects[0]) if self.lhs_prt2 else 0

    def get_rhs_prt1_len(self) -> int:
        return len(MathTex(self.rhs_prt1).submobjects[0]) if self.rhs_prt1 else 0

    def get_rhs_prt2_len(self) -> int:
        return len(MathTex(self.rhs_prt2).submobjects[0]) if self.rhs_prt2 else 0

    def get_lhs_prt1_range(self) -> tuple[int, int]:
        return (0, self.get_lhs_prt1_len())

    def get_lhs_prt2_range(self) -> tuple[int, int]:
        start_index = self.get_lhs_prt1_len()
        return (start_index, start_index + self.get_lhs_prt2_len())

    def get_rhs_prt1_range(self) -> tuple[int, int]:
        # Must add one due to equal sign
        start_index = self.get_lhs_prt1_len() + self.get_lhs_prt2_len() + 1
        return (start_index, start_index + self.get_rhs_prt1_len())

    def get_rhs_prt2_range(self) -> tuple[int, int]:
        # Once again have to add one due to the equal sign
        start_index = self.get_lhs_prt1_len() + self.get_lhs_prt2_len() + self.get_rhs_prt1_len() + 1
        return (start_index, start_index + self.get_rhs_prt2_len())

    def get_equal_sign_index(self) -> int:
        return self.get_lhs_prt1_len() + self.get_lhs_prt2_len()

    def update_mobject(self) -> None:
        # Initializes MathTex object
        super().__init__(self.get_string())

        # Set colors of MathTex object
        VGroup(self[0].submobjects[slice(*self.get_lhs_prt1_range())]).set_color(self.lhs_prt1_color)
        VGroup(self[0].submobjects[slice(*self.get_lhs_prt2_range())]).set_color(self.lhs_prt2_color)
        VGroup(self[0].submobjects[slice(*self.get_rhs_prt1_range())]).set_color(self.rhs_prt1_color)
        VGroup(self[0].submobjects[slice(*self.get_rhs_prt2_range())]).set_color(self.rhs_prt2_color)

        # Update Position to center equal sign on screen center
        equal_sign_glyph = self[0].submobjects[self.get_equal_sign_index()]
        pos_diff = self.tex_location - equal_sign_glyph.get_center()
        self.shift(pos_diff)

    def become_transform_target(self):
        assert self.transform_target is not None, "No transform target found"

        # Copy all kwargs from self.transform_target over
        kwargs = {}
        kwargs["tex_location"] = self.transform_target.tex_location
        kwargs["lhs_prt1"] = self.transform_target.lhs_prt1
        kwargs["lhs_prt2"] = self.transform_target.lhs_prt2
        kwargs["rhs_prt1"] = self.transform_target.rhs_prt1
        kwargs["rhs_prt2"] = self.transform_target.rhs_prt2
        kwargs["lhs_prt1_color"] = self.transform_target.lhs_prt1_color
        kwargs["lhs_prt2_color"] = self.transform_target.lhs_prt2_color
        kwargs["rhs_prt1_color"] = self.transform_target.rhs_prt1_color
        kwargs["rhs_prt2_color"] = self.transform_target.rhs_prt2_color

        # Reinitialize VariableVal to regenerate all submobject glyphs with attributes taken from self.transform_target
        # Can't use self.become() due to a lower length of submobjects in the self.transform_target mobject causing
        # ghost mobjects
        self.__init__(**kwargs)
        # self.submobjects = self.transform_target.submobjects

        # self.transform_target = None

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
                # dest_rhs_prt2_range is not mentioned here, since it is assumed that it should be empty.
                # I can't really include it as an introducer, as an empty entry will cause errors in MF_Tools
            ]
        else:
            transformation_tuples = [
                (list(src_lhs_prt1_range), list(dest_lhs_prt1_range)),
                ([self.get_equal_sign_index()], [self.transform_target.get_equal_sign_index()]),
                (list(src_rhs_prt1_range), list(dest_rhs_prt1_range)),
                (list(src_lhs_prt2_range), list(dest_rhs_prt2_range), {"path_arc": PI}),
                # See above comment for lack of src_rhs_prt2_range
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
            # Clean all submobjects from scene to add them back after reinitializing self to self.transform_target
            scene.add(self.mobA)
            scene.remove(self.mobA)

            # Cleanse all remaining orphaned submobjects from introducers
            # You do not comprehend the amounts of debugging I had to do to find
            # this incredibly hacky solution inside an already existing monkey patch
            scene.add(self.mobB)
            scene.remove(self.mobB)
            scene.remove(self.mobB.family)

            self.mobA.become_transform_target()

            scene.add(self.mobA)
            scene.remove(self.mobA)
            # scene.add(self.mobA)

        animation.clean_up_from_scene = patched_clean_up_meth.__get__(animation)

        return animation

class TestVariableVal(Slide):
    def construct(self):
        self.variable_val = VariableVal(UP * 3, "x", "", "5")
        transform_1 = self.variable_val.return_translate_animation(new_lhs_prt2="-3", perform_arithmetic=True)
        self.play(transform_1)

        self.wait()

        transform_2 = self.variable_val.return_translate_animation(new_lhs_prt2="", new_rhs_prt2="+3", perform_arithmetic=False)
        self.play(transform_2)

        self.wait()

        transform_3 = self.variable_val.return_translate_animation(new_rhs_prt1="8", new_rhs_prt2="", perform_arithmetic=True)
        self.play(transform_3)

        self.wait()

        # transform_4 = self.variable_val.return_translate_animation(new_lhs_prt2="+9", new_rhs_prt2="", perform_arithmetic=True)
        # self.play(transform_4)
        #
        # transform_5 = self.variable_val.return_translate_animation(new_lhs_prt2="", new_rhs_prt2="-9", perform_arithmetic=False)
        # self.play(transform_5)

        self.wait()

        transform_6 = self.variable_val.return_translate_animation(new_rhs_prt1="-1", new_rhs_prt2="", perform_arithmetic=True)
        self.play(transform_6)

        self.wait()

        self.play(
            *(Circumscribe(current_mobject) for current_mobject in self.variable_val.submobjects[0])
        )

        self.wait()

        transform_7 = self.variable_val.return_translate_animation(new_rhs_prt1="5", perform_arithmetic=True)
        self.play(transform_7)
