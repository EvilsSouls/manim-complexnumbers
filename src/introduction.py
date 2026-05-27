import numpy as np
from manim import *
from manim_slides import Slide
import MF_Tools as mf_tools

class IntroduceNumberSystems(Slide):
    def construct(self):
        self.start_skip_animations()
        # TODO: Natürliche Zahlen
        self.next_slide(notes="Vorstellen wir sind in der Grundschule: Hier haben wir alle natürliche Zahlen")

        ORIGIN_NAT_NUMS = LEFT * 6.75
        START_VAL = 5
        SPACING = 0.95

        nat_dots = VGroup()

        for i in range(0, 18):
            dot = Dot(point=ORIGIN_NAT_NUMS + RIGHT * i * SPACING, color=YELLOW)
            dot_label = Tex(f"{i}").next_to(dot, UP)
            nat_dots.add(VGroup(dot, dot_label))

        self.play(
            AnimationGroup(*[Create(point_label) for point_label in nat_dots], lag_ratio=0.5, run_time=1)
        )


        self.next_slide(notes="Normale Arithmetische Operationen: Addition, Subtraktion, Multiplikation, Division, **etc.**")

        def show_arithmetic_binary_operation(val_a: int, operation: str, val_b: int, val_c: int, commutative = True):
            tex = MathTex(str(val_a), operation, str(val_b), '=', str(val_c)).shift(UP * 3)

            tex[0].set_color(BLUE)
            tex[2].set_color(BLUE if commutative else PURPLE)
            tex[4].set_color(GREEN)

            operand1_dot = nat_dots[val_a]
            operand2_dot = nat_dots[val_b]
            result_dot = nat_dots[val_c]

            self.play(Write(VGroup(tex.submobjects[0:2])), Indicate(operand1_dot, color=BLUE, scale_factor=2), run_time=0.75)
            self.play(Write(VGroup(tex.submobjects[2:4])), Indicate(operand2_dot, color=BLUE if commutative else PURPLE, scale_factor=2), run_time=0.75)
            self.play(Write(VGroup(tex.submobjects[4])), Indicate(result_dot, color=GREEN, scale_factor=2), run_time=0.75)

            return tex

        sum_example_tex = show_arithmetic_binary_operation(5, '+', 8, 13)

        self.next_slide() # Remove Sum Example & Show Difference Example
        self.play(FadeOut(sum_example_tex, shift=DOWN * 0.5), run_time=0.25)
        diff_example_tex = show_arithmetic_binary_operation(9, '-', 7, 2, False)

        self.next_slide()
        self.play(FadeOut(diff_example_tex, shift=DOWN * 0.5), run_time=0.25)
        prod_example_tex = show_arithmetic_binary_operation(7, r'\cdot', 2, 14)

        self.next_slide()
        self.play(FadeOut(prod_example_tex, shift=DOWN * 0.5), run_time=0.25)
        quot_example_tex = show_arithmetic_binary_operation(6, r'\div', 3, 2, False)

        self.wait(1)
        self.play(FadeOut(quot_example_tex, shift=DOWN * 0.5), run_time=0.25)


        self.next_slide(notes="Doch wenn wir uns der einfachste Operator—die Addition—noch mal anschauen, kann man schnell ein Problem erkennen. \n\n Wir definieren eine Zahl x, die bei 5 beginnt")

        # Create Arrow pointing at the number currently mirrored by ValueTracker with label showing current target number
        value_tracker = ValueTracker(START_VAL)

        pointer_loc = ORIGIN_NAT_NUMS + RIGHT * value_tracker.get_value() * SPACING # TODO: Abstract into function
        pointer = Arrow(start=pointer_loc + 2 * DOWN, end=pointer_loc, buff=0.3)

        label = MathTex("x").add_updater(lambda m: m.next_to(pointer, DOWN))
        pointer_label = VGroup(pointer, label)

        pointer.add_updater(lambda m: m.move_to(ORIGIN_NAT_NUMS + RIGHT * value_tracker.get_value() * SPACING + DOWN)) # TODO: Abstract

        self.play(Create(pointer_label))

        variable_val = MathTex(f"x = {START_VAL:.0f}").shift(UP*3)
        self.play(Write(variable_val), run_time=0.5)


        self.stop_skip_animations()
        self.next_slide(notes="Man sieht wie Addition als Gleiten entlang des Zahlenstrahls wahrgenommen werden kann; Warte bis Stehen Geblieben!", loop=True)

        def slide_incr(val, run_time):
            formatted_val_string = f"{'+' if val >= 0 else ''}" + str(val)

            # Align Brace to invisible line that spans the entire sliding animation
            line = Line(ORIGIN_NAT_NUMS + RIGHT * value_tracker.get_value() * SPACING + 2 * DOWN, ORIGIN_NAT_NUMS + RIGHT * (value_tracker.get_value() + val) * SPACING + 2 * DOWN)
            br = Brace(line, buff=0.5, sharpness=2, color=RED_E)
            label = MathTex(formatted_val_string, color=RED).next_to(br, DOWN)

            # New Variable val with added summand (x = 3 + 2)
            new_variable_val = MathTex(f"x = {value_tracker.get_value():.0f} {formatted_val_string}").shift(UP*3).align_to(variable_val, LEFT)
            summand_glyph_range = np.arange(len(variable_val[0]), len(new_variable_val[0])) # The range of all glyph indices for the newly added summand
            for i in summand_glyph_range: new_variable_val[0][i].set_color(RED)

            self.play(FadeIn(br, shift=UP),
                      FadeIn(label, shift=UP),
                      mf_tools.TransformByGlyphMap(variable_val, new_variable_val,
                                          ([0, 1, 2], [0, 1, 2]),
                                          ([], list(summand_glyph_range)),
                                          # introduce_individually=True,
                                          default_introducer=Write),
                      run_time=0.4)

            self.wait(0.3)

            # New Variable Val with updated number
            newer_variable_val = MathTex(f"x = {value_tracker.get_value() + val:.0f}").shift(UP*3)
            result_glyph_range = np.arange(2, len(newer_variable_val[0])) # The new number starts at index 2, due to index 0 and 1 being x= (sorry for the magic number)

            self.play(value_tracker.animate.increment_value(val),
                      mf_tools.TransformByGlyphMap(new_variable_val, newer_variable_val,
                                          ([0, 1], [0, 1]),
                                                   (list(np.insert(summand_glyph_range, 0, range(2, len(variable_val[0])))), list(result_glyph_range))),
                      run_time=run_time)

            self.play(Transform(br, pointer_label.copy()), Transform(label, pointer_label.copy()), run_time=0.33)
            self.remove(br, label)

            return newer_variable_val # Cursed; Should abstract to seperate methods

        # self.play(value_tracker.animate.increment_value(1), run_time=0.75)
        variable_val = slide_incr(1, 0.75)
        self.wait(0.5)

        # self.play(value_tracker.animate.increment_value(-3), run_time=0.75)
        variable_val = slide_incr(-3, 0.75)
        self.wait(0.5)

        # self.play(value_tracker.animate.increment_value(7), run_time=0.75)
        variable_val = slide_incr(7, 0.75)
        self.wait(0.5)

        # self.play(value_tracker.animate.increment_value(-5), run_time=1.25)
        variable_val = slide_incr(-5, 1.5)
        self.wait(3)
