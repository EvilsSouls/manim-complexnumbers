from manim import *
from manim.mobject.text.tex_mobject import MathTexPart
from manim.animation.transform import _MethodAnimation

from manim.typing import Vector3DLike
from manim.utils.color import ManimColor
from typing import cast

from enum import Enum

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
        *,
        separator="=",
    ):
        self.tex_location = tex_location

        self._l1_str = lhs_prt1
        self._l2_str = lhs_prt2
        self._r1_str = rhs_prt1
        self._r2_str = rhs_prt2

        self.separator = separator

        self.zero_width_char = r"\hskip 0pt"

        self.l1_color = lhs_prt1_color
        self.l2_color = lhs_prt2_color
        self.r1_color = rhs_prt1_color
        self.r2_color = rhs_prt2_color

        self.transform_target: None | VariableVal = None

        self.PartIndices = Enum("PartIndices", [
            ("L1_INDEX", 0),
            ("L2_INDEX", 1),
            ("EQ_INDEX", 2),
            ("R1_INDEX", 3),
            ("R2_INDEX", 4)
        ])

        # Only change if you know what you're doing. Quite a lot of stuff is specificially
        # hardcoded for a specific type of animation
        self.INTRODUCE_ANIMATION = Write
        self.TRANSFORM_ANIMATION = Transform
        # Couldn't use FadeOut, due to it *having* to be a remover (which is undesired
        # behavior, since that would remove one of the submobjects of self, which is something
        # I *do not* want to deal with (I've had trouble with that before))
        # Also I couldn't use FadeTransform due to that causing the object to shift *and* fade,
        # which is also undesired (however, instead, because of my visual perfectionism)
        self.remover_animation = lambda mobj, **animation_kwargs: mobj.animate(**animation_kwargs).set_fill(opacity=0)

        self.update_mobject()

    # Set setters and getters to automatically use a 0-width latex character instead of an empty string
    @property
    def l1_str(self):
        """The l1_str property."""
        return self._l1_str if self._l1_str else self.zero_width_char

    @l1_str.setter
    def l1_str(self, value):
        self._l1_str = value


    @property
    def l2_str(self):
        """The l2_str property."""
        return self._l2_str if self._l2_str else self.zero_width_char

    @l2_str.setter
    def l2_str(self, value):
        self._l2_str = value


    @property
    def r1_str(self):
        """The r1_str property."""
        return self._r1_str if self._r1_str else self.zero_width_char

    @r1_str.setter
    def r1_str(self, value):
        self._r1_str = value


    @property
    def r2_str(self):
        """The r2_str property."""
        return self._r2_str if self._r2_str else self.zero_width_char

    @r2_str.setter
    def r2_str(self, value):
        self._r2_str = value

    def get_l1_mobj(self) -> MathTexPart:
        return cast(MathTexPart, self.submobjects[self.PartIndices.L1_INDEX.value])

    def get_l2_mobj(self) -> MathTexPart:
        return cast(MathTexPart, self.submobjects[self.PartIndices.L2_INDEX.value])

    def get_equal_sign_mobj(self) -> MathTexPart:
        return cast(MathTexPart, self.submobjects[self.PartIndices.EQ_INDEX.value])

    def get_r1_mobj(self) -> MathTexPart:
        return cast(MathTexPart, self.submobjects[self.PartIndices.R1_INDEX.value])

    def get_r2_mobj(self) -> MathTexPart:
        return cast(MathTexPart, self.submobjects[self.PartIndices.R2_INDEX.value])

    def update_mobject(self) -> None:
        # Initialize MathTex object, with each part being its own SingleStringMathTex object
        super().__init__(self.l1_str, self.l2_str, self.separator, self.r1_str, self.r2_str)

        # Set colors of SingleStringMathTex objects
        self.get_l1_mobj().set_color(self.l1_color)
        self.get_l2_mobj().set_color(self.l2_color)
        self.get_r1_mobj().set_color(self.r1_color)
        self.get_r2_mobj().set_color(self.r2_color)

        # Update Position to center equal sign on screen center
        pos_diff = self.tex_location - self.get_equal_sign_mobj().get_center()
        self.shift(pos_diff)

    # def become_transform_target(self):
    #     assert self.transform_target is not None, "No transform target found"
    #
    #     # Copy all kwargs from self.transform_target over
    #     kwargs = {}
    #     kwargs["tex_location"] = self.transform_target.tex_location
    #     kwargs["lhs_prt1"] = self.transform_target.lhs_prt1
    #     kwargs["lhs_prt2"] = self.transform_target.lhs_prt2
    #     kwargs["rhs_prt1"] = self.transform_target.rhs_prt1
    #     kwargs["rhs_prt2"] = self.transform_target.rhs_prt2
    #     kwargs["lhs_prt1_color"] = self.transform_target.lhs_prt1_color
    #     kwargs["lhs_prt2_color"] = self.transform_target.lhs_prt2_color
    #     kwargs["rhs_prt1_color"] = self.transform_target.rhs_prt1_color
    #     kwargs["rhs_prt2_color"] = self.transform_target.rhs_prt2_color
    #
    #     # Reinitialize VariableVal to regenerate all submobject glyphs with attributes taken from self.transform_target
    #     # Can't use self.become() due to a lower length of submobjects in the self.transform_target mobject causing
    #     # ghost mobjects
    #     self.__init__(**kwargs)
    #     # self.submobjects = self.transform_target.submobjects
    #
    #     # self.transform_target = None

    def process_animate_part(self, animation_list: list[Animation], src_mobj, dest_mobj, **animation_kwargs):
        # Process delay copied to https://github.com/TheMathematicFanatic/MF_Tools/blob/91760a6a7d69f88235034ef043a93a2d12c18b81/src/MF_Tools/transforms.py#L155
        delay = animation_kwargs.pop("delay", 0)
        if delay != 0:
            run_time = animation_kwargs.pop("run_time", 1)
            new_run_time = delay + run_time
            rate_func = animation_kwargs.pop("rate_func", smooth)
            def new_rate_func(t): # https://www.desmos.com/calculator/4hphvny63n
                a = delay / new_run_time
                if t < a:
                    return 0
                else:
                    return rate_func((t-a)/(1-a))
            animation_kwargs["rate_func"] = new_rate_func
            animation_kwargs["run_time"] = new_run_time

        def is_empty(mobj):
            is_empty_condition = lambda tex_part: not tex_part or tex_part.tex_string == self.zero_width_char

            if type(mobj) is VGroup:
                result = True

                for current_submobj in mobj.submobjects:
                    if not is_empty_condition(current_submobj):
                        result = False
                    else:
                        # Remove empty glyphs, since they cause
                        # weird glitchy behavior when transforming
                        mobj.submobjects.remove(current_submobj)

                return result

            return is_empty_condition(mobj)

        if is_empty(src_mobj):
            if is_empty(dest_mobj):
                print(f"Empty src ({src_mobj}) and dest ({dest_mobj})")
                return
            else:
                print(f"Animation (from: {src_mobj} to {dest_mobj}) is Introducer")
                # src_mobj.align_data(cast(VariableVal, self.transform_target))
                # src_mobj.interpolate(src_mobj, self.transform_target, 1)
                animation_list.append(self.INTRODUCE_ANIMATION(dest_mobj, **animation_kwargs))
        else:
            if is_empty(dest_mobj):
                print(f"Animation (from: {src_mobj} to {dest_mobj}) is Remover")
                # Opacity gets set back to one, once all of submobjects of self have been updated
                # to reflect the new changes that couldn't be done using Transform
                animation_list.append(self.remover_animation(src_mobj, **animation_kwargs))
            else:
                print(f"Animation translates from {src_mobj} to {dest_mobj}")
                animation_list.append(self.TRANSFORM_ANIMATION(src_mobj, dest_mobj, **animation_kwargs))

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
    ) -> AnimationGroup:

        kwargs = {}
        kwargs["tex_location"] = self.tex_location if new_tex_location is None else new_tex_location
        kwargs["lhs_prt1"] = self._l1_str if new_lhs_prt1 is None else new_lhs_prt1
        kwargs["lhs_prt2"] = self._l2_str if new_lhs_prt2 is None else new_lhs_prt2
        kwargs["rhs_prt1"] = self._r1_str if new_rhs_prt1 is None else new_rhs_prt1
        kwargs["rhs_prt2"] = self._r2_str if new_rhs_prt2 is None else new_rhs_prt2
        kwargs["lhs_prt1_color"] = self.l1_color if new_lhs_prt1_color is None else new_lhs_prt1_color
        kwargs["lhs_prt2_color"] = self.l2_color if new_lhs_prt2_color is None else new_lhs_prt2_color
        kwargs["rhs_prt1_color"] = self.r1_color if new_rhs_prt1_color is None else new_rhs_prt1_color
        kwargs["rhs_prt2_color"] = self.r2_color if new_rhs_prt2_color is None else new_rhs_prt2_color

        self.transform_target = VariableVal(**kwargs)

        animations: list[Animation] = []

        if perform_arithmetic:
            self.process_animate_part(animations, self.get_l1_mobj(), self.transform_target.get_l1_mobj())
            self.process_animate_part(animations, self.get_l2_mobj(), self.transform_target.get_l2_mobj(), delay=0.5)
            self.process_animate_part(animations, self.get_equal_sign_mobj(), self.transform_target.get_equal_sign_mobj())
            self.process_animate_part(animations, VGroup(self.get_r1_mobj(), self.get_r2_mobj()), self.transform_target.get_r1_mobj())
            self.process_animate_part(animations, None, self.transform_target.get_r2_mobj())
        else:
            self.process_animate_part(animations, self.get_l1_mobj(), self.transform_target.get_l1_mobj())
            self.process_animate_part(animations, self.get_equal_sign_mobj(), self.transform_target.get_equal_sign_mobj())
            self.process_animate_part(animations, self.get_r1_mobj(), self.transform_target.get_r1_mobj())
            self.process_animate_part(animations, self.get_l2_mobj(), self.transform_target.get_r2_mobj(), path_arc=PI)
            self.process_animate_part(animations, None, self.transform_target.get_l2_mobj())

        animation = AnimationGroup(*animations)

        # # Incredibly hacky monkey patching that overrides the default behavior, which assumes that
        # # ReplacementTransform or something similar is used, meaning that mobB should be added to
        # # the screen and the initial state of mobA reset
        # def patched_clean_up_meth(self, scene):
        #     pass
        #
        # animation.clean_up_from_scene = patched_clean_up_meth.__get__(animation)

        """
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
            # scene.remove(self.mobB.get_family())

            self.mobA.become_transform_target()

            # scene.add(self.mobA)
            # scene.remove(self.mobA)
            scene.add(self.mobA)

        animation.clean_up_from_scene = patched_clean_up_meth.__get__(animation)

        return animation
        """

        return animation
