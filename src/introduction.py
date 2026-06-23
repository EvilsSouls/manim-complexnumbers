import math
from variable_val import VariableVal

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
        school_icon = SVGMobject("assets/school-opensvg-dot-dev.svg", fill_color=GRAY_A, stroke_color=GRAY_A, fill_opacity=1, width=5).shift(UP)
        label = Text("Zurück in die Grundschule (yay?)", font_size=50).next_to(school_icon, DOWN, buff=1.25)
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

        self.next_slide(auto_next=True)
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
        self.value_tracker = mft.VT(self.START_VAL)

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
                  mft.TransformByGlyphMap(
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
        self.play(
            self.value_tracker.animate.increment_value(val),
            mft.TransformByGlyphMap(
                new_variable_val, newest_variable_val,
                ([0, 1], [0, 1]),
                (list(summands_glyph_range), list(result_glyph_range))
            ),
            run_time=run_time,
        )

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

        # Move to 'undefined' place (-1)
        self.slide_incr(-2, 1, self.qm_variable_val)


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
        new_environment = MathTex(r"\mathbb{Z}", font_size=65).set_color(YELLOW).to_corner(UL, buff=0.25)
        self.play(
            AnimationGroup(
                *[AnimationGroup(GrowFromCenter(point_label['d']), Write(point_label['l'])) for point_label in reversed_neg_nums],
                lag_ratio=neg_nums_lag_ratio,
                run_time=neg_nums_run_time
            ),
            mft.TransformByGlyphMap(
                self.variable_val,
                corrected_variable_val,
                ([0, 1], [0, 1]),
                auto_morph=True,
                run_time=neg_nums_run_time*0.75
            ),
            # Idea and Implementation of Transformation Animation provided by @nmbj on Discord
            self.current_environment.animate(remover=True, run_time=neg_nums_run_time*0.75).scale((1,0,1), about_edge=UP),
            new_environment.save_state().scale((1,0,1), about_edge=DOWN).animate(introducer=True, run_time=neg_nums_run_time*0.75).restore()
        )

        # Sort number_dots
        self.number_dots.sort(submob_func=lambda dot_with_label: dot_with_label['d'].get_center()[0])

        # Because TransformByGlyphMap must use ReplacementTransform for some reason, we need this assignment
        self.variable_val = corrected_variable_val
        # And because the manual transformation between the old and new number environment
        # did not update the old variable, we must assign self.current_environment ourselves as well
        self.current_environment = new_environment

    def introduction_rational_numbers(self):
        new_variable_val = MathTex(f"x={self.START_VAL}").shift(self.TEX_LOC)

        self.play(
            self.value_tracker @ 5,
            mft.TransformByGlyphMap(
                self.variable_val,
                new_variable_val,
                ([0, 1], [0, 1]),
                auto_morph=True
            )
        )

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
        self.next_slide("Wir setzen unsere Variable zu 5 zurück") # TODO: Somehow replace this with Jonas Weinmarkt analogy perhaps
        self.introduction_rational_numbers()
