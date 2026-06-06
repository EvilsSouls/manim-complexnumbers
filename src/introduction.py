import math

import numpy as np
from manim import *
from manim_slides import Slide
import MF_Tools as mf_tools

from manim.typing import Vector3DLike

class IntroduceNumberSystems(Slide):
    def setup(self) -> None:
        # At the very start all natural numbers from 0 to self.END_NUM are displayed
        # (yes: 0 is a natural number — don't @ me)
        self.END_NUM = 15
        # self.origin_nat_nums * LEFT is where the '0' point of the number system is located
        # I previously had it simply set to 6.75 * LEFT, however since I need to move it to the right, when introducing whole numbers,
        # it must be a ValueTracker, which can't use a vector as its input
        self.origin_nat_nums = mf_tools.VT(6.75)

        self.START_VAL = 5
        self.SPACING = 0.95
        self.TEX_LOC = UP * 3
        self.POINTER_LENGTH = 2

        self.NAT_POINT_COLOR = YELLOW
        self.SUMMAND_COLOR = GREEN

    # Somewhat hacky fix, where sometimes the last frame does not get rendered when presenting
    def next_slide(self, *args, **kwargs):
        self.wait(0.001)
        super().next_slide(*args, **kwargs)

    def nl_to_coords(self, nl_val):
        return ~self.origin_nat_nums * LEFT + RIGHT * nl_val * self.SPACING

    # TODO: Add reference that these numbers are the natural numbers, such that it can change in the process (Natural Numbers perhaps fades into symbol that stays in the upper left corner)
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
        RESULT_COLOR: ParsableManimColor) -> None:

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
        self.value_tracker = ValueTracker(self.START_VAL)

        pointer_loc = self.nl_to_coords(self.value_tracker.get_value())
        self.pointer = Arrow(start=pointer_loc + self.POINTER_LENGTH * DOWN, end=pointer_loc, buff=0.3)
        self.pointer.add_updater(lambda m: m.move_to(self.nl_to_coords(self.value_tracker.get_value()) + 1/2 * self.POINTER_LENGTH * DOWN))

        self.pointer_label = MathTex("x").next_to(self.pointer, DOWN)
        self.play(AnimationGroup(GrowArrow(self.pointer), Write(self.pointer_label), lag_ratio = 0.5), run_time=POINTER_CREATION_TIME)

        # Only add updater after animation, so that it doesn't move with the growing pointer
        self.pointer_label.add_updater(lambda m: m.next_to(self.pointer, DOWN))

        self.variable_val = MathTex(f"x = {self.START_VAL:.0f}").shift(TEX_LOC)
        TEX_WRITING_TIME = POINTER_CREATION_TIME / 2
        self.play(Write(self.variable_val), run_time=TEX_WRITING_TIME)

    def slide_incr(self, val: float, run_time: float, result_variable_val_overwrite: MathTex | None = None):
        formatted_val_string = f"{'+' if val >= 0 else ''}" + str(val)

        # Align Brace to invisible line that spans the entire sliding animation
        line_loc_1 = self.nl_to_coords(self.value_tracker.get_value()) + self.POINTER_LENGTH * DOWN
        line_loc_2 = self.nl_to_coords(self.value_tracker.get_value() + val) + self.POINTER_LENGTH * DOWN
        line = Line(line_loc_1, line_loc_2)
        br = Brace(line, buff=0.5, sharpness=2, color=self.SUMMAND_COLOR) # MAGIC NUMBERS AAaaAAAAA
        label = MathTex(formatted_val_string, color=self.SUMMAND_COLOR).next_to(br, DOWN)

        # New Variable val with added summand (for example x = 3 + 2)
        new_variable_val = MathTex(f"x = {self.value_tracker.get_value():.0f} {formatted_val_string}").shift(self.TEX_LOC).align_to(self.variable_val, LEFT)
        summand_glyph_range = np.arange(len(self.variable_val[0]), len(new_variable_val[0])) # The range of all glyph indices for the newly added summand
        for i in summand_glyph_range: new_variable_val[0][i].set_color(self.SUMMAND_COLOR) # Set color of each glyph mobject individually TODO: vectorize perhaps

        # Fade in the Bracket and Label and add the Summand to the already existing label of the variable val
        self.play(FadeIn(br, shift=UP),
                  FadeIn(label, shift=UP),
                  mf_tools.TransformByGlyphMap(
                      self.variable_val, new_variable_val,
                      ([0, 1, 2], [0, 1, 2]),
                      ([], list(summand_glyph_range)),
                      introduce_individually=True,
                      default_introducer=Write),
                  run_time=0.4)

        self.wait(0.3)

        if result_variable_val_overwrite is None:
            # New Variable Val with updated number
            newest_variable_val = MathTex(f"x = {self.value_tracker.get_value() + val:.0f}").shift(self.TEX_LOC)
        else:
            newest_variable_val = result_variable_val_overwrite

        summands_glyph_range = np.arange(2, len(new_variable_val[0]))
        result_glyph_range = np.arange(2, len(newest_variable_val[0])) # The new number starts at glyph index 2, due to index 0 and 1 being x= (sorry for the magic number)

        # Move the pointer to the result of the sum / difference and transform the label of the variable val to reflect the actual result of the sum
        self.play(self.value_tracker.animate.increment_value(val),
                  mf_tools.TransformByGlyphMap(
                      new_variable_val, newest_variable_val,
                      ([0, 1], [0, 1]),
                      (list(summands_glyph_range), list(result_glyph_range))),
                  run_time=run_time)

        self.play(Transform(br, self.pointer.copy()), Transform(label, self.pointer.copy()), run_time=0.33)
        self.remove(br, label)

        self.variable_val = newest_variable_val

    def experimentation_add_subtract(self):
        self.slide_incr(1, 0.75)
        self.wait(0.5)

        self.slide_incr(-4, 0.75)
        self.wait(0.5)

        self.slide_incr(7, 0.75)
        self.wait(0.5)

        self.slide_incr(-8, 1)

    def introduction_whole_numbers(self, neg_nums_lag_ratio = 0.5, neg_nums_run_time = 2.5):
        # Shift all natural numbers, such that 0 is in the middle of the screen
        self.play(self.origin_nat_nums @ 0, run_time=1.5)
        # Remove all dots that are now not visible
        nat_dots_length = len(self.number_dots.submobjects)
        new_dots_len = math.ceil(nat_dots_length / 2) # Somewhat misleading, as soon the negative numbers will be added
        del self.number_dots.submobjects[new_dots_len:nat_dots_length]

        result_variable_val = MathTex(r"x = \text{\Large ?}").shift(self.TEX_LOC)
        # Set styling of question mark
        question_mark = result_variable_val[0][-1]
        question_mark.set_color(RED)
        question_mark.shift((result_variable_val[0][1].get_center()[1] - question_mark.get_center()[1]) * UP) # Vertically center question mark
        # Move to 'undefined' place
        self.slide_incr(-2, 1, result_variable_val)


        self.next_slide(notes="")

        # Create all the negative numbers
        for i in range(-new_dots_len + 1, 0):
            dot = Dot(point=self.nl_to_coords(i), color=self.NAT_POINT_COLOR)
            dot_label = Tex(f"{i}").next_to(dot, UP)
            # Shift the label, such that the number (without the sign) is centered above the dot
            dot_label.shift((dot.get_center()[0] - dot_label[0][1].get_center()[0]) * RIGHT)
            self.number_dots.add(VDict([('d', dot), ('l', dot_label)]))

        corrected_variable_val = MathTex(f"x = {self.value_tracker.get_value():.0f}").shift(self.TEX_LOC)
        reversed_neg_nums = self.number_dots[-1:new_dots_len-1:-1]
        self.play(
            AnimationGroup(
                *[AnimationGroup(GrowFromCenter(point_label['d']), Write(point_label['l'])) for point_label in reversed_neg_nums],
                lag_ratio=neg_nums_lag_ratio,
                run_time=neg_nums_run_time
            ),
            mf_tools.TransformByGlyphMap(
                self.variable_val,
                corrected_variable_val,
            )
        )

    def construct(self):
        # self.start_skip_animations()
        self.next_slide(notes="Vorstellen wir sind in der Grundschule: Hier haben wir alle natürliche Zahlen")
        self.animate_creation_natural_numbers()

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

        # self.stop_skip_animations()
        self.next_slide()
        self.introduction_whole_numbers()
