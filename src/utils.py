from manim.typing import Point3D

def clamp(num: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(max_val, num))

def clamp_loc_horiz(loc: Point3D, min_loc: Point3D, max_loc: Point3D) -> Point3D:
    loc[0] = clamp(loc[0], min_loc[0], max_loc[0])

    return loc
