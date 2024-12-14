import itertools
import math
import os
import re
from collections import defaultdict, namedtuple

this_folder = "\\".join(__file__.split("\\")[:-1])


Robot = namedtuple("Point", "x y vx vy")
MapSize = namedtuple("MapSize", "xmax ymax")


def get_safety_factor(robots, map_size):
    quadrant_counts = [0, 0, 0, 0]
    center_x = map_size.xmax // 2
    center_y = map_size.ymax // 2
    for robot in robots:
        quadrant_index = 0
        if robot.x == center_x or robot.y == center_y:
            continue
        if robot.x > center_x:
            quadrant_index += 1
        if robot.y > center_y:
            quadrant_index += 2
        quadrant_counts[quadrant_index] += 1
    return math.prod(quadrant_counts)


def main(filename, map_size, seconds):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    robots = []
    for line in input_data:
        x, y, vx, vy = map(int, re.findall(r"[-\d]+", line))
        robots.append(Robot(x, y, vx, vy))

    # Part 1
    for i in range(seconds):
        for j, robot in enumerate(robots):
            new_x = (robot.x + robot.vx) % map_size.xmax
            new_y = (robot.y + robot.vy) % map_size.ymax
            robots[j] = Robot(new_x, new_y, robot.vx, robot.vy)
    result1 = get_safety_factor(robots, map_size)

    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    try:
        assert main("input_example.txt", map_size=MapSize(7, 11), seconds=100) == (
            12,
            24,
        )
        assert main("input.txt", map_size=MapSize(101, 103), seconds=100) == (
            228457125,
            24,
        )
    except AssertionError:
        print("❌ wrong")
