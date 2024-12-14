import itertools
import math
import os
import re
import shutil
from collections import defaultdict, namedtuple
from time import sleep

import matplotlib.pyplot as plt
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

this_folder = "\\".join(__file__.split("\\")[:-1])


Robot = namedtuple("Point", "x y vx vy")
MapSize = namedtuple("MapSize", "xmax ymax")

OUTPUT = "output"


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


average_distance_to_center = []


def render(robots, map_size, time_elapsed):
    img = PIL.Image.new(mode="L", size=(map_size.xmax, map_size.ymax), color="white")
    average_distance = 0
    center_x = map_size.xmax // 2
    center_y = map_size.ymax // 2
    for robot in robots:
        img.putpixel((robot.x, robot.y), 0)
        average_distance += abs(robot.x - center_x) + abs(robot.y - center_y)
    average_distance_to_center.append(average_distance / len(robots))
    if average_distance_to_center[-1] == min(average_distance_to_center):
        draw = PIL.ImageDraw.Draw(img)
        font = PIL.ImageFont.truetype("arial.ttf", 12)
        draw.text((0, 0), f"{time_elapsed}", font=font, fill=0)
        img.save(f"{this_folder}/{OUTPUT}/{time_elapsed:04d}.png")


def main(filename, map_size, seconds, do_render):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    robots = []
    for line in input_data:
        x, y, vx, vy = map(int, re.findall(r"[-\d]+", line))
        robots.append(Robot(x, y, vx, vy))

    # Part 1

    if do_render:
        if os.path.exists(f"{this_folder}/{OUTPUT}"):
            shutil.rmtree(f"{this_folder}/{OUTPUT}")
        os.makedirs(f"{this_folder}/{OUTPUT}")
    for i in range(seconds):
        for j, robot in enumerate(robots):
            new_x = (robot.x + robot.vx) % map_size.xmax
            new_y = (robot.y + robot.vy) % map_size.ymax
            robots[j] = Robot(new_x, new_y, robot.vx, robot.vy)
        if do_render:
            print(f"Rendering {i+1}/{seconds}")
            render(robots, map_size, i + 1)
    if do_render:
        plt.figure(figsize=(10, 10))
        plt.plot(average_distance_to_center)
        # add label with x,y at minimum
        plt.xlabel("Elapsed time")
        plt.ylabel("Average distance to center")
        min_index = average_distance_to_center.index(min(average_distance_to_center))
        plt.annotate(
            f"{min_index+1}",
            (min_index, average_distance_to_center[min_index]),
        )
        plt.savefig(f"{this_folder}/average_distance_to_center.png")
        plt.close()
    result1 = get_safety_factor(robots, map_size)

    print(f"Part 1 {filename}: ", result1)
    return result1


if __name__ == "__main__":
    try:
        assert (
            main(
                "input_example.txt",
                map_size=MapSize(7, 11),
                seconds=100,
                do_render=False,
            )
            == 12
        )

        assert (
            main("input.txt", map_size=MapSize(101, 103), seconds=100, do_render=False)
            == 228457125
        )

        main("input.txt", map_size=MapSize(101, 103), seconds=10000, do_render=True)
    except AssertionError:
        print("❌ wrong")
