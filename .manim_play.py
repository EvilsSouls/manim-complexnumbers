from manim import *
from manim_slides import Slide

class IntroduceNumberSystems(Slide):
    def construct(self):
        self.next_section(skip_animations=True)
        ORIGIN_NAT_NUMS = LEFT * 7
        START_VAL = 5

        nat_dots = VGroup()

        for i in range(1, 20):
            dot = Dot(point=ORIGIN_NAT_NUMS + RIGHT * i, color=YELLOW)
            dot_label = Tex(f"{i}").next_to(dot, UP)
            nat_dots.add(VGroup(dot, dot_label))

        self.play(
            Succession(*[Create(point_label, run_time=0.1) for point_label in nat_dots], lag_ratio=0.5)
        )


        self.next_slide("Addition als Gleiten entlang des Zahlenstrahls der Natürlichen Zahlen", auto_next=True)

        value_tracker = ValueTracker(START_VAL)
        pointer = Arrow(start=ORIGIN_NAT_NUMS + RIGHT * value_tracker.get_value() + 2 * DOWN, end=ORIGIN_NAT_NUMS + RIGHT * value_tracker.get_value(), buff=0.3)
        label = MathTex("x").add_updater(lambda m: m.next_to(pointer, DOWN))
        pointer_label = VGroup(pointer, label)

        self.next_section()
        pointer.add_updater(lambda m: m.move_to(ORIGIN_NAT_NUMS + RIGHT * value_tracker.get_value() + DOWN))

        self.play(Create(pointer_label))

        variable_val = MathTex("x = ", f"{START_VAL}").shift(UP*3)
        self.play(Write(variable_val), run_time=0.5)

        self.wait(3)


        self.next_slide("Warte bis Stehen Geblieben!", loop=True)

        def slide_incr(val, run_time):
            line = Line(ORIGIN_NAT_NUMS + RIGHT * value_tracker.get_value() + 2 * DOWN, ORIGIN_NAT_NUMS + RIGHT * (value_tracker.get_value() + val) + 2 * DOWN)
            br = Brace(line, buff=0.5, sharpness=2, color=RED_E)
            label = MathTex(f"+{val if val >= 0 else f'({val})'}", color=RED).next_to(br, DOWN)

            self.play(FadeIn(br, shift=UP), FadeIn(label, shift=UP), run_time=0.25)

            new_variable_val = MathTex("x = ", f"{value_tracker.get_value() + val}").shift(UP*3)
            self.play(value_tracker.animate.increment_value(val), Transform(variable_val, new_variable_val), run_time=run_time)

            self.play(Transform(br, pointer_label.copy()), Transform(label, pointer_label.copy()), run_time=0.125)
            self.remove(br, label)

        # self.play(value_tracker.animate.increment_value(1), run_time=0.75)
        slide_incr(1, 0.75)
        self.wait(0.5)

        # self.play(value_tracker.animate.increment_value(-3), run_time=0.75)
        slide_incr(-3, 0.75)
        self.wait(0.5)

        # self.play(value_tracker.animate.increment_value(7), run_time=0.75)
        slide_incr(7, 0.75)
        self.wait(0.5)

        # self.play(value_tracker.animate.increment_value(-5), run_time=1.25)
        slide_incr(-5, 1.25)
        self.wait(3)
