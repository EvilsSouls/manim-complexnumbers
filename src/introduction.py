import math
from typing import final

from manim._config import logger_utils
from variable_val import VariableVal
from utils import clamp_loc_horiz

import numpy as np
from numpy.random import default_rng
from manim import *
from manim_slides import Slide
import MF_Tools as mft

from manim.typing import Vector3DLike

"""
@todo:
- Use Jonas Weinmarkt
- perhaps make class deterministic (seed)
"""

class IntroduceNumberSystems(Slide):
    def setup(self) -> None:
        # At the very start all natural numbers from 0 to self.END_NUM are displayed
        # (yes: 0 is a natural number — don't @ me)
        self.END_NUM = 15
        # self.origin_nat_nums * LEFT is where the '0' point of the number system is located
        # I previously had it simply set to 6.75 * LEFT, however since I need to move it to the right, when introducing whole numbers,
        # it must be a ValueTracker, which can't use a vector as its input
        self.origin_nat_nums = mft.VT(6.75)

        self.START_VAL = 5
        self.SPACING = 0.95
        self.TEX_LOC = UP * 3
        self.POINTER_LENGTH = 2

        self.NAT_POINT_COLOR = YELLOW
        self.SUMMAND_COLOR = RED

        # Variable Val Tex with Question Mark (used multiple times, when introducing new numbers)
        self.qm_variable_val = MathTex(r"x = \text{\large ?}").shift(self.TEX_LOC)
        # Set styling of question mark
        question_mark = self.qm_variable_val[0][-1]
        question_mark.set_color(RED)
        question_mark.shift((self.qm_variable_val[0][1].get_center()[1] - question_mark.get_center()[1]) * UP) # Vertically center question mark

        # We love gambling
        self.rng = default_rng()

    # Somewhat hacky fix, where sometimes the last frame does not get rendered when presenting
    def next_slide(self, *args, **kwargs):
        self.wait(0.001)
        super().next_slide(*args, **kwargs)

    def nl_to_coords(self, nl_val):
        return ~self.origin_nat_nums * LEFT + RIGHT * nl_val * self.SPACING

    def introduction(self, AMOUNT_NUMS):
        school_icon = SVGMobject("assets/school-opensvg-dot-dev.svg", fill_color=GRAY_A, stroke_color=WHITE, fill_opacity=1, width=5).shift(UP)
        label = Text("Zurück ins Paradies", font_size=50).next_to(school_icon, DOWN, buff=1.5)
        school_icon_label = VGroup(school_icon, label)
        self.play(Write(school_icon_label), run_time=2.5)

        self.next_slide("Wie heißt die Gruppe dieser Zahlen?") # TODO: Perhaps consider adding a vertical slide for a tip
        random_numbers = VGroup(MathTex(f"{rand_int}").move_to(3*mft.Vcis(i*TAU/AMOUNT_NUMS)) for (i, rand_int) in enumerate(np.append(self.rng.choice(np.arange(1, 100), size=AMOUNT_NUMS-1, replace=False), 0)))
        # Hacky
        self.play(ScaleInPlace(school_icon_label, 20), GrowFromCenter(random_numbers))
        self.remove(school_icon_label)

        self.next_slide(notes="Zunächst schauen wir uns *nur* die Natürlichen Zahlen an")

        nat_nums_txt = Text("Natürliche Zahlen")
        self.play(ReplacementTransform(random_numbers, nat_nums_txt, path_arc=PI))

        self.next_slide()
        self.current_environment = MathTex(r"\mathbb{N}", font_size=65).set_color(YELLOW).to_corner(UL, buff=0.25)
        self.play(ReplacementTransform(nat_nums_txt, self.current_environment))

    def animate_creation_natural_numbers(self, lag_ratio = 0.5, run_time = 1) -> None:
        self.number_dots = VGroup()

        # TODO: Perhaps consider replacing this with a simple align() call
        for i in range(0, self.END_NUM):
            dot = Dot(point=self.nl_to_coords(i), color=self.NAT_POINT_COLOR)
            dot_label = Tex(f"{i}").next_to(dot, UP)
            self.number_dots.add(VDict([('d', dot), ('l', dot_label)]))

        # Store a refernce to the '0' dot, for future reference (when negative numbers are added)
        # This is technically not needed, since the negative dots will be added after the positive ones and will as such not be needed,
        # but I'd rather not deal wit that and simply have an easy-to-read reference
        self.zero_dot = self.number_dots[0]['d']

        self.play(
            AnimationGroup(*[AnimationGroup(GrowFromCenter(point_label['d']), Write(point_label['l'])) for point_label in self.number_dots], lag_ratio=lag_ratio, run_time=run_time)
        )

        # The Group has to be added to the scene for animations and updaters on the entire group to function
        self.add(self.number_dots)

        # Always move the dots to the location defined by self.origin_nat_nums
        # Credit to the Example Gallery for idea on how to implement this (https://docs.manim.community/en/stable/examples.html#movinggrouptodestination)
        self.number_dots.add_updater(lambda dots: dots.shift(self.nl_to_coords(0) - self.zero_dot.get_center()))

    def show_example_arithmetic_operations(
        self,
        TEX_LOC: Vector3DLike,
        DOTS_SCALE_FACTOR: float,
        WRITE_RUN_TIME: float,
        OPERAND1_COLOR: ParsableManimColor,
        OPERAND2_COLOR: ParsableManimColor,
        RESULT_COLOR: ParsableManimColor
    ) -> None:

        def show_arithmetic_binary_operation(val_a: int, operation: str, val_b: int, val_c: int, commutative = True):
            operand2_color = OPERAND1_COLOR if commutative else OPERAND2_COLOR

            tex = MathTex(str(val_a), operation, str(val_b), '=', str(val_c)).shift(TEX_LOC)

            tex[0].set_color(OPERAND1_COLOR)
            tex[2].set_color(operand2_color)
            tex[4].set_color(RESULT_COLOR)

            operand1_dot = self.number_dots[val_a]
            operand2_dot = self.number_dots[val_b]
            result_dot = self.number_dots[val_c]

            indicate_dots = [(operand1_dot, OPERAND1_COLOR), (None, None), (operand2_dot, operand2_color), (None, None), (result_dot, RESULT_COLOR)]

            animations = []
            for (i, current_glyph) in enumerate(tex.submobjects):
                current_dot, current_dot_indicate_color = indicate_dots[i]
                if current_dot:
                    animations.append(AnimationGroup(Write(current_glyph), Indicate(current_dot, color=current_dot_indicate_color, scale_factor=DOTS_SCALE_FACTOR)))
                else:
                    animations.append(Write(current_glyph))

            self.play(
                AnimationGroup(*[animations], lag_ratio = 0.5),
                run_time=WRITE_RUN_TIME
            )

            return tex

        FADE_OUT_TIME = WRITE_RUN_TIME / 9

        sum_example_tex = show_arithmetic_binary_operation(5, '+', 8, 13)

        self.next_slide() # Remove Sum Example & Show Difference Example
        self.play(FadeOut(sum_example_tex, shift=DOWN * 0.5), run_time=FADE_OUT_TIME)
        diff_example_tex = show_arithmetic_binary_operation(9, '-', 7, 2, False)

        self.next_slide()
        self.play(FadeOut(diff_example_tex, shift=DOWN * 0.5), run_time=FADE_OUT_TIME)
        prod_example_tex = show_arithmetic_binary_operation(7, r'\cdot', 2, 14)

        self.next_slide()
        self.play(FadeOut(prod_example_tex, shift=DOWN * 0.5), run_time=FADE_OUT_TIME)
        quot_example_tex = show_arithmetic_binary_operation(6, r'\div', 3, 2, False)

        self.wait(1)
        self.play(FadeOut(quot_example_tex, shift=DOWN * 0.5), run_time=FADE_OUT_TIME)

    def prepare_experimentation_add_subtract(self, TEX_LOC, POINTER_CREATION_TIME):
        # Create Arrow pointing at the number currently mirrored by ValueTracker with label showing current target number
        self.value_tracker = mft.VT(self.START_VAL)

        pointer_loc = self.nl_to_coords(self.value_tracker.get_value())
        self.pointer = Arrow(start=pointer_loc + self.POINTER_LENGTH * DOWN, end=pointer_loc, buff=0.3)
        self.pointer.add_updater(lambda m: m.move_to(self.nl_to_coords(self.value_tracker.get_value()) + 1/2 * self.POINTER_LENGTH * DOWN))

        self.pointer_label = MathTex("x").next_to(self.pointer, DOWN)
        self.play(AnimationGroup(GrowArrow(self.pointer), Write(self.pointer_label), lag_ratio = 0.5), run_time=POINTER_CREATION_TIME)

        # Only add updater after animation, so that it doesn't move with the growing pointer
        self.pointer_label.add_updater(lambda m: m.next_to(self.pointer, DOWN))

        self.variable_val = MathTex(f"x = {self.START_VAL:.0f}").shift(TEX_LOC)
        self.variable_val = VariableVal(TEX_LOC, "x", "", f"{self.START_VAL:.0f}")
        TEX_WRITING_TIME = POINTER_CREATION_TIME / 2
        self.play(Write(self.variable_val), run_time=TEX_WRITING_TIME)

    def slide_incr(self, val: float, run_time: float, unknown_result = False):
        def format_val_string(val):
            return f"{'+' if val >= 0 else ''}" + str(val)

        self.increment_vals.append(val)

        lhs_summand_transform = self.variable_val.return_translate_animation(new_lhs_prt2=format_val_string(-val), perform_arithmetic=True)
        self.play(lhs_summand_transform, run_time=1.5)

        self.next_slide()

        # Align Brace to invisible line that spans the entire sliding animation
        line_loc_1 = self.nl_to_coords(self.value_tracker.get_value()) + self.POINTER_LENGTH * DOWN
        line_loc_2 = self.nl_to_coords(self.value_tracker.get_value() + val) + self.POINTER_LENGTH * DOWN
        line = Line(line_loc_1, line_loc_2)
        br = Brace(line, buff=0.5, sharpness=2, color=self.SUMMAND_COLOR) # MAGIC NUMBERS AAaaAAAAA
        label = MathTex(format_val_string(val), color=self.SUMMAND_COLOR).next_to(br, DOWN)

        # New Variable val with added summand (for example x = 3 + 2)
        rhs_summand_transform = self.variable_val.return_translate_animation(new_lhs_prt2="", new_rhs_prt2=format_val_string(val), perform_arithmetic=False)

        # Fade in the Bracket and Label and add the Summand to the already existing label of the variable val
        self.play(
            FadeIn(br, shift=UP),
            FadeIn(label, shift=UP),
            rhs_summand_transform,
            run_time=1.5
        )

        self.wait(0.3)

        if unknown_result is False:
            # Transform to the sum of both summands
            transform_to_sum = self.variable_val.return_translate_animation(new_rhs_prt1=f"{self.value_tracker.get_value() + val:.0f}", new_rhs_prt2="", perform_arithmetic=True)
        else:
            transform_to_sum = self.variable_val.return_translate_animation(new_rhs_prt1=r"\text{\large ?}", new_rhs_prt2="", new_rhs_prt1_color=RED, perform_arithmetic=True)

        # Move the pointer to the result of the sum / difference and transform the label of the variable val to reflect the actual result of the sum
        self.play(
            self.value_tracker.animate.increment_value(val),
            transform_to_sum,
            run_time=run_time,
        )

        self.play(Transform(br, self.pointer.copy()), Transform(label, self.pointer.copy()), run_time=0.33)
        self.remove(br, label)

    def experimentation_add_subtract(self):
        self.increment_vals = []

        self.slide_incr(1, 0.75)
        self.next_slide()

        self.slide_incr(-5, 0.75)
        self.next_slide()

        self.slide_incr(2, 0.75)

    def introduction_whole_numbers(self, neg_nums_lag_ratio = 0.5, neg_nums_run_time = 2.5):
        # Shift all natural numbers, such that 0 is in the middle of the screen
        self.play(self.origin_nat_nums @ 0, run_time=1.5)
        # Remove all dots that are now not visible
        nat_dots_length = len(self.number_dots.submobjects)
        new_dots_len = math.ceil(nat_dots_length / 2) # Somewhat misleading, as soon the negative numbers will be added
        del self.number_dots.submobjects[new_dots_len:nat_dots_length]

        # Move to 'undefined' place (-1)
        self.slide_incr(-4, 1, True)

        self.next_slide(notes="")

        # Create all the negative numbers
        for i in range(-new_dots_len + 1, 0):
            dot = Dot(point=self.nl_to_coords(i), color=self.NAT_POINT_COLOR)
            dot_label = Tex(f"{i}").next_to(dot, UP)
            # Shift the label, such that the number (without the sign) is centered above the dot
            dot_label.shift((dot.get_center()[0] - dot_label[0][1].get_center()[0]) * RIGHT)
            self.number_dots.add(VDict([('d', dot), ('l', dot_label)]))

        transform_to_corrected_variable_val = self.variable_val.return_translate_animation(new_rhs_prt1=f"{self.value_tracker.get_value():.0f}", new_rhs_prt1_color=WHITE, perform_arithmetic=True)
        reversed_neg_nums = self.number_dots[-1:new_dots_len-1:-1]
        new_environment = MathTex(r"\mathbb{Z}", font_size=65).set_color(YELLOW).to_corner(UL, buff=0.25)
        self.play(
            AnimationGroup(
                *[AnimationGroup(GrowFromCenter(point_label['d']), Write(point_label['l'])) for point_label in reversed_neg_nums],
                lag_ratio=neg_nums_lag_ratio,
                run_time=neg_nums_run_time
            ),
            transform_to_corrected_variable_val,
            # Idea and Implementation of Transformation Animation provided by @nmbj on Discord
            self.current_environment.animate(remover=True, run_time=neg_nums_run_time*0.75).scale((1,0,1), about_edge=UP),
            new_environment.save_state().scale((1,0,1), about_edge=DOWN).animate(introducer=True, run_time=neg_nums_run_time*0.75).restore()
        )

        # Sort number_dots
        self.number_dots.sort(submob_func=lambda dot_with_label: dot_with_label['d'].get_center()[0])

        # And because the manual transformation between the old and new number environment
        # did not update the old variable, we must assign self.current_environment ourselves as well
        self.current_environment = new_environment

    def introduction_rational_numbers(self, rational_nums_run_time = 2.5):
        ARROW_START = DOWN * 0.5
        ARROW_BUFFER = 0.4

        # Fade Out Pointer to give space to the displacement arrows
        self.play(FadeOut(self.pointer, self.pointer_label, self.variable_val), run_time=0.5)
        self.wait(0.5)

        # Create Displacement Arrows to eventually show the cumulative sum of all increments
        self.displacement_arrows = VGroup()
        current_val = 0
        for i, current_increment_val in enumerate(self.increment_vals):
            # Create Arrow
            new_current_val = current_val + current_increment_val
            arrow = Arrow(self.nl_to_coords(current_val), self.nl_to_coords(new_current_val), stroke_width=4, color=RED, buff=0)

            # Stack on top of eachother
            arrow.shift(ARROW_START + DOWN * i * ARROW_BUFFER)

            # Create Label and darken background of arrow at label's position
            displacement_arrow_label = MathTex(current_increment_val, font_size=35, color=RED).move_to(arrow.get_center())
            label_background = BackgroundRectangle(displacement_arrow_label, fill_opacity=0.9, buff=0.1)

            # Play Creation of Arrow
            self.play(LaggedStart(GrowArrow(arrow), AnimationGroup(FadeIn(label_background, run_time=0.1), FadeIn(displacement_arrow_label)), lag_ratio=0.6), run_time=1)
            self.displacement_arrows += VDict([("a", arrow), ("l", VGroup(label_background, displacement_arrow_label))])

            current_val = new_current_val

        self.next_slide()

        # Flatten out all of the lines to create their sum
        flatten_arrows_animations = []
        final_sum_result = sum(self.increment_vals)
        # The label of the resulting line must be calculated before the line itself, for the Translation target of the labels to be defined
        resulting_line_label = MathTex(*(f"{'+' if val >= 0 else ''}{val}" for val in self.increment_vals), font_size=35, color=RED)
        # Move to estimated position
        resulting_line_label.move_to(1/2 * (self.zero_dot.get_center() + self.nl_to_coords(final_sum_result)))
        resulting_line_label.align_to(ARROW_START, UP)
        resulting_line_label.shift(1/2 * ARROW_BUFFER * DOWN)
        for i, current_arrow in enumerate(self.displacement_arrows):
            old_line_start = current_arrow['a'].get_start()
            old_line_end = current_arrow['a'].get_end()

            # Remove any excess line parts outside of the range [final_sum_result,0] or [0,final_sum_result] depending on the sign of final_sum_result
            if final_sum_result < 0:
                old_line_start = clamp_loc_horiz(old_line_start, self.nl_to_coords(final_sum_result), self.zero_dot.get_center())
                old_line_end = clamp_loc_horiz(old_line_end, self.nl_to_coords(final_sum_result), self.zero_dot.get_center())
            else:
                old_line_start = clamp_loc_horiz(old_line_start, self.zero_dot.get_center(), self.nl_to_coords(final_sum_result))
                old_line_end = clamp_loc_horiz(old_line_end, self.zero_dot.get_center(), self.nl_to_coords(final_sum_result))

            new_joined_line = Line(old_line_start, old_line_end, color=RED)
            new_joined_line.align_to(ARROW_START, UP) # Align all lines vertically ontop of eachother

            # Add a tip to the very last line
            if i == len(self.displacement_arrows) - 1:
                new_joined_line.add_tip(tip_shape=ArrowTriangleFilledTip)

            flatten_arrows_animations.append(AnimationGroup(
                Transform(current_arrow['a'], new_joined_line),
                FadeOut(current_arrow['l'][0]),
                Transform(current_arrow['l'][1], resulting_line_label[i], path_arc=-PI)
            ))

        self.play(AnimationGroup(*flatten_arrows_animations, lag_ratio=0.1), run_time=2)

        # Create the new resulting line *before* actually faltting out all of the arrows, to be able to translate the labels to the correct position
        new_resulting_line = Line(self.displacement_arrows[0]['a'].get_start(), self.displacement_arrows[-1]['a'].get_end(), color=RED)
        new_resulting_line.add_tip(tip_shape=ArrowTriangleFilledTip)
        # # Correct the placement of resulting_line_label now that the location of the new_resulting_line is known.
        # # Shouldn't actually change anything, but there is no reason why not to try to correct it
        # resulting_line_label.next_to(new_resulting_line, DOWN, buff=0.1)
        # nvm... won't be able to know the exact location of label, without calculating the position of new_resulting_line first,
        # which in this case is too much effort (it probably would be quite trivial... I'd just have to switch to ReplacementTransform
        # (to be able to use the already calculated positions before playing the actual Animation, but eh... I am fine with just hardcoding
        # an estimated location)

        for current_arrow in self.displacement_arrows.submobjects:
            self.remove(current_arrow['a'])
            self.remove(current_arrow['l'][1])
        del self.displacement_arrows

        self.add(new_resulting_line, resulting_line_label)

        # self.stop_skip_animations()

        self.next_slide()

        increment_length = len(self.increment_vals)
        scaled_num = final_sum_result / increment_length
        scaled_line = Arrow(self.zero_dot.get_center(), self.nl_to_coords(scaled_num), color=GREEN, buff=0, stroke_width=1.5, max_tip_length_to_length_ratio=0.2).align_to(ARROW_START, UP)
        new_label = MathTex(f"{{{final_sum_result}", r"\over", f"{increment_length}}}", "=", r"\text{\large ?}", font_size=35).next_to(scaled_line, DOWN, buff=0.1)
        new_label[0:3].set_color(GREEN)
        new_label[-1].set_color(RED)

        following_dot = Dot(ORIGIN, color=GREEN, radius=DEFAULT_DOT_RADIUS * 0.9).set_z_index(-1)
        following_dot.add_updater(lambda mobj: mobj.move_to(new_resulting_line.get_end()[0] * RIGHT))
        self.add(following_dot)

        self.variable_val.__init__(tex_location=self.TEX_LOC, lhs_prt1=r"\mu", rhs_prt1=r"\text{\large ?}", lhs_prt1_color=GREEN, rhs_prt1_color=RED)

        self.play(
            mft.TransformByGlyphMap(
                resulting_line_label,
                new_label,
                (list(range(0,increment_length)), [0], {"run_time": 2.5}),
                ([], [1], {"run_time": 2.5}),
                ([], [2], {"run_time": 2.5}),
                ([], [3, 4], {"delay": 2.5, "run_time": 0.25, "shift": None}),
                mobA_submobject_index=[],
                mobB_submobject_index=[],
                shift_fades=True,
                run_time=2.75,
                introduce_individually=False,
            ),
            ReplacementTransform(new_resulting_line, scaled_line, run_time=2.5),
            Write(self.variable_val, run_time=2.5),
        )

        following_dot.set_z_index(1)

        self.next_slide()

        new_environment = MathTex(r"\mathbb{Q}", font_size=65).set_color(YELLOW).to_corner(UL, buff=0.25)

        max_num = math.floor(self.END_NUM / 2)
        self.number_line = NumberLine(
            [-max_num, max_num + 0.5, 1], # Add space for tip
            unit_size=self.SPACING,
            color=self.NAT_POINT_COLOR,
            include_numbers=True,
            label_direction=UP,
            include_tip=True,
            tip_width=0.25,
            tip_height=0.25,
        )
        # Align number line to previous dots
        self.number_line.shift(self.number_dots[0]['d'].get_center() - self.number_line.get_start())
        # Add smaller half-step ticks
        # Don't need to subtract SMALLER_TICK_STEP, since the last value is always excluded
        SMALLER_TICK_STEP = 0.5
        for current_tick_val in np.arange(-max_num + SMALLER_TICK_STEP, max_num, SMALLER_TICK_STEP): 
            if not current_tick_val.is_integer():
                current_tick = self.number_line.get_tick(current_tick_val, 0.1 * 0.5)
                self.number_line.get_tick_marks().add(current_tick)
        # Sort the ticks so that the VGroup contains the ticks in a left-to-right order
        self.number_line.get_tick_marks().sort(submob_func=lambda tick: tick.get_center()[0])

        self.value_tracker @= scaled_num
        self.pointer.update().set_color(GREEN)
        # Used to correctly align the actual self.pointer_label
        self.abs_pointer_label = MathTex(str(abs(scaled_num)), font_size=35).next_to(self.pointer, DOWN, buff=0.2)
        self.pointer_label = MathTex(str(scaled_num), font_size=35).set_color(GREEN).move_to(self.abs_pointer_label.get_center())

        variable_val_transform_animation = self.variable_val.return_translate_animation(new_rhs_prt1=str(scaled_num), new_rhs_prt1_color=WHITE, perform_arithmetic=True)

        self.play(
            *((
                (
                    ReplacementTransform(current_dot['l'], self.number_line.numbers[i]),
                    ReplacementTransform(current_dot['d'], self.number_line.get_tick_marks()[int((1/SMALLER_TICK_STEP) * i)])
                )
            ) for i, current_dot in enumerate(self.number_dots)),

            variable_val_transform_animation,
            ReplacementTransform(new_label, self.pointer_label, path_arc=-np.pi/2, suspend_mobject_updating=True),
            ReplacementTransform(scaled_line, self.pointer, path_arc=-np.pi/2),

            *(GrowFromCenter(self.number_line.get_tick_marks()[i]) for i in range(1, len(self.number_line.get_tick_marks()), int(1/SMALLER_TICK_STEP))),
            DrawBorderThenFill(self.number_line.get_tip()),
            GrowFromPoint(self.number_line.save_state().set(submobjects=[]), point=self.zero_dot.get_center()),

            # Idea and Implementation of Transformation Animation once again provided by @nmbj on Discord
            self.current_environment.animate(remover=True, run_time=rational_nums_run_time*0.75).scale((1,0,1), about_edge=UP),
            new_environment.save_state().scale((1,0,1), about_edge=DOWN).animate(introducer=True, run_time=rational_nums_run_time*0.75).restore(),

            run_time=3
        )

        # Restore Numberline to once again contain submobjects
        self.number_line.restore()
        self.current_environment = new_environment

        self.wait()

        self.add(self.number_line)

        # Somehow have to add updater after playing animation, since the mobjects in self.pointer_label.submobjects apparently
        # get replaced with functions that automatically update the mobjects submobjects
        self.abs_pointer_label.add_updater(lambda mobj: mobj.next_to(self.pointer, DOWN))
        self.pointer_label.add_updater(lambda mobj: mobj.move_to(self.abs_pointer_label.get_center()))

        self.wait()


    def construct(self):
        # self.start_skip_animations()
        self.next_slide()
        self.introduction(16)

        self.animate_creation_natural_numbers(run_time=2)

        ## Probably won't use this.
        ## I fear it might not actually be relevant to the actual presentation and might only serve to distract the listener from what I am saying.
        ## See 'math videos online — any advice' question on https://www.3blue1brown.com/about#faqs
        ## (I had already had my reservations on including this, due to the point mentioned in the advice (specifically under 'avoid pointless animations'),
        ## but still was unsure about it).
        ## I do think it might be helpful, to slow my talking down.
        ## If I need to wait for this animation, it might remind me to pause when speaking and think about what I say next.
        ## Perhaps I should simply experiment with including it and not including it, when I practice (TODO)

        # self.next_slide(notes="Normale Arithmetische Operationen: Addition, Subtraktion, Multiplikation, Division, **etc.**")
        # DOTS_SCALE_FACTOR = 2
        # WRITE_RUN_TIME = 2.25
        # OPERAND1_COLOR = BLUE
        # OPERAND2_COLOR = PURPLE
        # RESULT_COLOR = GREEN
        # self.show_example_arithmetic_operations(self.TEX_LOC, DOTS_SCALE_FACTOR, WRITE_RUN_TIME, OPERAND1_COLOR, OPERAND2_COLOR, RESULT_COLOR)

        self.next_slide(notes="Doch wenn wir etwas mit den einfachsten Operatoren—die Addition und Subtraktion—rumexperimentieren, kann man schnell ein Problem erkennen. \n\n Wir definieren eine Zahl x, die bei 5 beginnt")
        POINTER_CREATION_TIME = 1
        self.prepare_experimentation_add_subtract(self.TEX_LOC, POINTER_CREATION_TIME)

        self.next_slide(notes="Man sieht wie Addition als Gleiten entlang des Zahlenstrahls wahrgenommen werden kann; Warte bis Stehen Geblieben!")
        self.experimentation_add_subtract()

        self.next_slide()
        self.introduction_whole_numbers()

        # self.stop_skip_animations()

        self.next_slide("Wir setzen unsere Variable zu 5 zurück") # TODO: Somehow replace this with Jonas Weinmarkt analogy perhaps — Wants to get average amount of money he spent each day
        self.introduction_rational_numbers()
