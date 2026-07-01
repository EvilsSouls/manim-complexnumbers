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
        # Needed to keep track of some Mobjects that have to be removed once finished
        self.to_be_removed = []

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
        self.TRANSFORM_ANIMATION = ReplacementTransform
        self.REMOVER_ANIMATION = FadeOut

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

    def become_transform_target(self):
        assert self.transform_target is not None, "No transform target found"

        self.align_data(self.transform_target)
        # self.interpolate(self, self.transform_target, 1)
        self.submobjects = self.transform_target.submobjects

        self.tex_location = self.transform_target.tex_location

        self._l1_str = self.transform_target._l1_str
        self._l2_str = self.transform_target._l2_str
        self._r1_str = self.transform_target._r1_str
        self._r2_str = self.transform_target._r2_str

        self.separator = self.transform_target.separator

        self.l1_color = self.transform_target.l1_color
        self.l2_color = self.transform_target.l2_color
        self.r1_color = self.transform_target.r1_color
        self.r2_color = self.transform_target.r2_color

        self.transform_target = None
        self.to_be_removed = []

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
                self.to_be_removed.append(mobj)

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
                return
            else:
                # animation_list.append(self.INTRODUCE_ANIMATION(dest_mobj, **animation_kwargs))
                animation_list.append(Write(dest_mobj, remover=True, **animation_kwargs))
        else:
            if is_empty(dest_mobj):
                # Opacity gets set back to one, once all of submobjects of self have been updated
                # to reflect the new changes that couldn't be done using Transform
                animation_list.append(self.REMOVER_ANIMATION(src_mobj, **animation_kwargs))
            else:
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
        setattr(animation, "original_parent_mobject", self)

        # Incredibly hacky monkey patching that overrides the default behavior, which assumes that
        # ReplacementTransform or something similar is used, meaning that mobB should be added to
        # the screen and the initial state of mobA reset
        def patched_clean_up_meth(self, scene):
            super(AnimationGroup, self).clean_up_from_scene(scene)

            scene.add(self.original_parent_mobject)
            scene.remove(self.original_parent_mobject)
            scene.add(*self.original_parent_mobject.to_be_removed)
            scene.remove(*self.original_parent_mobject.to_be_removed)

            self.original_parent_mobject.become_transform_target()

            scene.remove(self.original_parent_mobject)
            scene.add(self.original_parent_mobject)

        animation.clean_up_from_scene = patched_clean_up_meth.__get__(animation)

        return animation
