from manim import *
from manim.mobject.text.tex_mobject import MathTexPart
from manim.animation.transform import _MethodAnimation

from manim.typing import Vector3DLike
from manim.utils.color import ManimColor
from typing import Any, cast

from enum import Enum

type CustomTransformTarget = tuple[str, str] | tuple[str, str, dict[str, Any]]

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
            ("L1", 0),
            ("L2", 1),
            ("EQ", 2),
            ("R1", 3),
            ("R2", 4)
        ])

        # Only change if you know what you're doing. Quite a lot of stuff is specificially
        # hardcoded for a specific type of animation
        self.introduce_animation = Write
        self.transform_animation = ReplacementTransform
        self.remove_animation = FadeOut

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
        return cast(MathTexPart, self.submobjects[self.PartIndices.L1.value])

    def get_l2_mobj(self) -> MathTexPart:
        return cast(MathTexPart, self.submobjects[self.PartIndices.L2.value])

    def get_equal_sign_mobj(self) -> MathTexPart:
        return cast(MathTexPart, self.submobjects[self.PartIndices.EQ.value])

    def get_r1_mobj(self) -> MathTexPart:
        return cast(MathTexPart, self.submobjects[self.PartIndices.R1.value])

    def get_r2_mobj(self) -> MathTexPart:
        return cast(MathTexPart, self.submobjects[self.PartIndices.R2.value])

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

    def process_animate_part(
        self,
        animation_list: list[Animation],
        src_mobj: Mobject | None,
        dest_mobj: Mobject | None,
        *,
        transform_animation,
        introduce_animation,
        remove_animation,
        **animation_kwargs
    ):
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

        def is_empty(mobj: Mobject | None):
            is_empty_condition = lambda tex_part: not tex_part or tex_part.tex_string == self.zero_width_char

            # If mobj is VGroup, check whether all of the submobjects are empty. If so, the parent object is
            # considered empty. If a single submobject, however, is not empty, the parent mobject is not
            # considered empty
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
                # animation_list.append(self.introduce_animation(dest_mobj, **animation_kwargs))
                animation_list.append(introduce_animation(dest_mobj, remover=True, **animation_kwargs))
        else:
            if is_empty(dest_mobj):
                # Opacity gets set back to one, once all of submobjects of self have been updated
                # to reflect the new changes that couldn't be done using Transform
                animation_list.append(remove_animation(src_mobj, **animation_kwargs))
            else:
                animation_list.append(transform_animation(src_mobj, dest_mobj, **animation_kwargs))

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
        combine_rhs: bool | None = None,
        custom_transform_target: CustomTransformTarget | list[CustomTransformTarget] | None = None,
        custom_transform_animation: Animation | None = None,
        custom_introduce_animation: Animation | None = None,
        custom_remove_animation: Animation | None = None,
        **transform_kwargs,
    ) -> AnimationGroup:
        """
        Any arguments left empty will default to the value of self
        """

        transform_animation = self.transform_animation if custom_transform_animation is None else custom_transform_animation
        introduce_animation = self.introduce_animation if custom_introduce_animation is None else custom_introduce_animation
        remove_animation = self.remove_animation if custom_remove_animation is None else custom_remove_animation

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

        print(f"transform target string: {self.transform_target.get_tex_string()}")

        animations: list[Animation] = []

        # Default behavior is transforming each respective part from self to its counterpart on self.transform_target.
        # If combine_rhs is additionally set (default behavior), then rhs_prt1 and rhs_prt2 get combined into rhs_prt1 of self.transform_target
        if custom_transform_target is None:
            if combine_rhs == None: combine_rhs = True

            self.process_animate_part(animations, self.get_l1_mobj(), self.transform_target.get_l1_mobj(),
                                      introduce_animation=introduce_animation,
                                      remove_animation=remove_animation,
                                      transform_animation=transform_animation
                                      )

            self.process_animate_part(animations, self.get_l2_mobj(), self.transform_target.get_l2_mobj(),
                                      introduce_animation=introduce_animation,
                                      remove_animation=remove_animation,
                                      transform_animation=transform_animation,
                                      delay=0.5
                                      )

            self.process_animate_part(animations, self.get_equal_sign_mobj(),
                                      self.transform_target.get_equal_sign_mobj(),
                                      introduce_animation=introduce_animation,
                                      remove_animation=remove_animation,
                                      transform_animation=transform_animation
                                      )

            self.process_animate_part(
                animations,
                VGroup(self.get_r1_mobj(), self.get_r2_mobj()) if combine_rhs else self.get_r1_mobj(),
                self.transform_target.get_r1_mobj(),
                introduce_animation=introduce_animation,
                remove_animation=remove_animation,
                transform_animation=transform_animation
            )

            self.process_animate_part(
                animations,
                None if combine_rhs else self.get_r2_mobj(),
                self.transform_target.get_r2_mobj(),
                introduce_animation=introduce_animation,
                remove_animation=remove_animation,
                transform_animation=transform_animation
            )
        else:
            source_indices = set()
            target_indices = set()

            if type(custom_transform_target) is tuple:
                custom_transform_target = [custom_transform_target]

            if combine_rhs == None: combine_rhs = False

            # Handle Custom Transform Targets
            for current_custom_transform_target in cast(list[CustomTransformTarget], custom_transform_target):
                if len(current_custom_transform_target) == 3:
                    custom_source, custom_target, custom_transform_kwargs = current_custom_transform_target
                elif len(current_custom_transform_target) == 2:
                    custom_source, custom_target = current_custom_transform_target
                    custom_transform_kwargs = {}
                else:
                    raise Exception("Invalid Custom Transform Target Length")

                # Keep Track of all of the parts that have custom connections
                source_indices.add(custom_source)
                target_indices.add(custom_target)

                automatic_path_arc = np.pi if abs(self.PartIndices[custom_target].value - self.PartIndices[custom_source].value > 1) else 0

                merged_kwargs = {"path_arc": automatic_path_arc}
                merged_kwargs |= custom_transform_kwargs

                if custom_transform_kwargs:
                    merged_kwargs = {"path_arc": automatic_path_arc} | custom_transform_kwargs
                else:
                    merged_kwargs = {"path_arc": automatic_path_arc}

                self.process_animate_part(
                    animations,
                    self.submobjects[self.PartIndices[custom_source].value],
                    self.transform_target.submobjects[self.transform_target.PartIndices[custom_target].value], # Using self.transform_target.PartIndices shouldn't make a difference
                    introduce_animation=introduce_animation,
                    remove_animation=remove_animation,
                    transform_animation=transform_animation,
                    **merged_kwargs
                )

                print(f"Custom Transform: from {custom_source} to {custom_target}")

            # If a custom connection is created between a source part p and a different target part q,
            # then the same part of the transform_target as the source part p, will be orphaned, as no
            # source part will now transform into it.
            # As such any and all defined source_indices will have an orphaned target at their same position,
            # as long as a custom target_index from a different connection is not also defined.
            orphaned_targets = source_indices.difference(target_indices)
            orphaned_sources = target_indices.difference(source_indices)

            # If R1 and R2 of source get combined into R1 of target, then R2 of target is orphaned, as long as there is no
            # custom connection towards it
            if combine_rhs and not "R2" in target_indices: orphaned_targets.add("R2")

            bound_parts = set(current_part.name for current_part in self.PartIndices).difference(source_indices, target_indices)

            for current_orphan in orphaned_targets:
                if current_orphan is not "R1" or not combine_rhs:
                    # All other parts will simply be a direct translation from self to
                    # self.transform_target (e.g. L1 of self will directly get translated to L1 of transform_target).
                    # However, as custom_source of self does not translate to custom_source of transform_target, custom_source
                    # of target must get introduced (if it exists, which in most cases it doesn't)
                    self.process_animate_part(
                        animations,
                        None,
                        self.transform_target.submobjects[self.transform_target.PartIndices[current_orphan].value], # Using self.transform_target.PartIndices shouldn't make a difference
                        introduce_animation=introduce_animation,
                        remove_animation=remove_animation,
                        transform_animation=transform_animation,
                    )

            for current_orphan in orphaned_sources:
                if current_orphan is not "R2" or not combine_rhs:
                    # Same thing as above if statement but for removers. For perhaps a better insight see .../docs/variable_val_schematic.svg
                    self.process_animate_part(
                        animations,
                        self.submobjects[self.PartIndices[current_orphan].value],
                        None,
                        introduce_animation=introduce_animation,
                        remove_animation=remove_animation,
                        transform_animation=transform_animation,
                    )

                    print(f"Removing Part {current_orphan}")

            for current_part in bound_parts:
                if not current_part == "R1" or not combine_rhs:
                    self.process_animate_part(
                        animations,
                        self.submobjects[self.PartIndices[current_part].value],
                        self.transform_target.submobjects[self.transform_target.PartIndices[current_part].value],
                        introduce_animation=introduce_animation,
                        remove_animation=remove_animation,
                        transform_animation=transform_animation,
                    )
                else:
                    self.process_animate_part(
                        animations,
                        VGroup(self.get_r1_mobj(), self.get_r2_mobj()),
                        self.transform_target.get_r1_mobj(),
                        introduce_animation=introduce_animation,
                        remove_animation=remove_animation,
                        transform_animation=transform_animation,
                    )

        print(f"Animations: {animations}")

        animation = AnimationGroup(*animations)
        setattr(animation, "original_parent_mobject", self)

        # Incredibly hacky monkey patching that overrides the default behavior, which assumes that
        # ReplacementTransform or something similar is used, meaning that mobB should be added to
        # the screen and the initial state of mobA reset
        def patched_clean_up_meth(self, scene):
            AnimationGroup.clean_up_from_scene(self, scene)

            scene.add(self.original_parent_mobject)
            scene.remove(self.original_parent_mobject)
            scene.add(*self.original_parent_mobject.to_be_removed)
            scene.remove(*self.original_parent_mobject.to_be_removed)

            self.original_parent_mobject.become_transform_target()

            scene.remove(self.original_parent_mobject)
            scene.add(self.original_parent_mobject)

        animation.clean_up_from_scene = patched_clean_up_meth.__get__(animation)

        return animation
