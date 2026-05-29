import numpy as np
from manim import *
from manim_slides import Slide
import MF_Tools as mf_tools

from manim.typing import Vector3DLike

class IntroduceNumberSystems(Slide):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.ORIGIN_NAT_NUMS = LEFT * 6.75
        self.START_VAL = 5
        self.SPACING = 0.95
        self.TEX_LOC = UP * 3
        self.POINTER_LENGTH = 2

        self.NAT_POINT_COLOR = YELLOW

    # Sometimes the last frame does not get rendered, when presenting
    def next_slide(self, *args, **kwargs):
        self.wait(0.001)
        super().next_slide(*args, **kwargs)

    def nl_to_coords(self, nl_val):
        return self.ORIGIN_NAT_NUMS + RIGHT * nl_val * self.SPACING

    # TODO: Add reference that these numbers are the natural numbers, such that it can change in the process (Natural Numbers perhaps fades into symbol that stays in the upper left corner)
    def animate_creation_natural_numbers(self, END_NUM: int, lag_ratio = 0.5, run_time = 1) -> None:
        self.nat_dots = VGroup()

        for i in range(0, END_NUM):
            dot = Dot(point=self.nl_to_coords(i), color=self.NAT_POINT_COLOR)
            dot_label = Tex(f"{i}").next_to(dot, UP)
            self.nat_dots.add(VDict([('d', dot), ('l', dot_label)]))

        self.play(
            AnimationGroup(*[AnimationGroup(GrowFromCenter(point_label['d']), Write(point_label['l'])) for point_label in self.nat_dots], lag_ratio=lag_ratio, run_time=run_time)
        )

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

            operand1_dot = self.nat_dots[val_a]
            operand2_dot = self.nat_dots[val_b]
            result_dot = self.nat_dots[val_c]

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

    def experimentation_add_subtract(self, SUMMAND_COLOR: ParsableManimColor):
        def slide_incr(val, run_time):
            formatted_val_string = f"{'+' if val >= 0 else ''}" + str(val)

            # Align Brace to invisible line that spans the entire sliding animation
            line_loc_1 = self.nl_to_coords(self.value_tracker.get_value()) + self.POINTER_LENGTH * DOWN
            line_loc_2 = self.nl_to_coords(self.value_tracker.get_value() + val) + self.POINTER_LENGTH * DOWN
            line = Line(line_loc_1, line_loc_2)
            br = Brace(line, buff=0.5, sharpness=2, color=SUMMAND_COLOR) # MAGIC NUMBERS AAaaAAAAA
            label = MathTex(formatted_val_string, color=SUMMAND_COLOR).next_to(br, DOWN)

            # New Variable val with added summand (for example x = 3 + 2)
            new_variable_val = MathTex(f"x = {self.value_tracker.get_value():.0f} {formatted_val_string}").shift(self.TEX_LOC).align_to(self.variable_val, LEFT)
            summand_glyph_range = np.arange(len(self.variable_val[0]), len(new_variable_val[0])) # The range of all glyph indices for the newly added summand
            for i in summand_glyph_range: new_variable_val[0][i].set_color(SUMMAND_COLOR) # Set color of each glyph mobject individually

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

            # New Variable Val with updated number
            newer_variable_val = MathTex(f"x = {self.value_tracker.get_value() + val:.0f}").shift(self.TEX_LOC)
            summands_glyph_range = np.arange(2, len(new_variable_val[0]))
            result_glyph_range = np.arange(2, len(newer_variable_val[0])) # The new number starts at index 2, due to index 0 and 1 being x= (sorry for the magic number)

            # Move the pointer to the result of the sum / difference and transform the label of the variable val to reflect the actual result of the sum
            self.play(self.value_tracker.animate.increment_value(val),
                      mf_tools.TransformByGlyphMap(
                          new_variable_val, newer_variable_val,
                          ([0, 1], [0, 1]),
                          (list(summands_glyph_range), list(result_glyph_range))),
                      run_time=run_time)

            self.play(Transform(br, self.pointer.copy()), Transform(label, self.pointer.copy()), run_time=0.33)
            self.remove(br, label)

            self.variable_val = newer_variable_val

        slide_incr(1, 0.75)
        self.wait(0.5)

        slide_incr(-3, 0.75)
        self.wait(0.5)

        slide_incr(7, 0.75)
        self.wait(0.5)

        slide_incr(-5, 1.5)
        self.wait(3)

    def construct(self):
        self.next_slide(notes="Vorstellen wir sind in der Grundschule: Hier haben wir alle natürliche Zahlen")
        END_NUM = 15
        self.animate_creation_natural_numbers(END_NUM)

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

        self.next_slide(notes="Doch wenn wir uns der einfachste Operator—die Addition—noch mal anschauen, kann man schnell ein Problem erkennen. \n\n Wir definieren eine Zahl x, die bei 5 beginnt")
        POINTER_CREATION_TIME = 1
        self.prepare_experimentation_add_subtract(self.TEX_LOC, POINTER_CREATION_TIME)

        self.next_slide(notes="Man sieht wie Addition als Gleiten entlang des Zahlenstrahls wahrgenommen werden kann; Warte bis Stehen Geblieben!", loop=True)
        SUMMAND_COLOR = RED
        self.experimentation_add_subtract(SUMMAND_COLOR)
