from manim import DEFAULT_MOBJECT_TO_MOBJECT_BUFFER, VGroup, MarkupText, DOWN, FadeTransform, Mobject

from manim.typing import Point3D

def clamp(num: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(max_val, num))

def clamp_loc_horiz(loc: Point3D, min_loc: Point3D, max_loc: Point3D) -> Point3D:
    loc[0] = clamp(loc[0], min_loc[0], max_loc[0])

    return loc

def center_markup_text(*strings, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER, **kwargs):
    """
    Can't really figure out how to add a good type annotation to this.
    However, a single 'string' inside *strings may be of two types:
        - a simple string; or
        - a dictionary containing the actual string in the 'line' attribute
          and additional attributes that will be passed to MarkupText as **kwargs

    **kwargs to center_markup_text will be passed to all MarkupText objects
    """
    string_group = VGroup()

    for current_string in strings:
        if type(current_string) is str:
            new_obj = MarkupText(current_string, **kwargs)
            string_group.add(new_obj)
        elif type(current_string) is dict:
            raw_string = current_string.pop('line')
            new_obj = MarkupText(raw_string, **current_string, **kwargs)
            string_group.add(new_obj)

    string_group.arrange(DOWN, buff)

    return string_group
