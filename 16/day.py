from collections import namedtuple

this_folder = "\\".join(__file__.split("\\")[:-1])

WALL = "#"
FREE = "."

START = "S"
END = "E"

COST_FORWARD = 1
COST_ROTATE = 1000

Loc = namedtuple("Loc", ["x", "y"])


def find(map, something):
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == something:
                return Loc(x, y)
    raise ValueError(f"Could not find {something} in map")


ROTATION_OPTIONS = {
    (0, 1): [(1, 0), (-1, 0)],
    (1, 0): [(0, -1), (0, 1)],
    (0, -1): [(1, 0), (-1, 0)],
    (-1, 0): [(0, -1), (0, 1)],
}


def sum_tuple(t1, t2):
    return Loc(t1[0] + t2[0], t1[1] + t2[1])


def moves_to_make(loc, orient):
    options = [(sum_tuple(loc, orient), orient, COST_FORWARD)]
    for opt in ROTATION_OPTIONS[orient]:
        options.append((loc, opt, COST_ROTATE))
    return options


LOWEST_COST_PER_LOC_ORIENT = {}


def heuristig_cost(loc, direction, goal):
    diff_x = goal[0] - loc[0]
    diff_y = goal[1] - loc[1]

    dir_x = direction[0]
    dir_y = direction[1]

    if dir_x == 1 and diff_x > 0 and diff_y == 0:
        return diff_x * COST_FORWARD
    if dir_x == -1 and diff_x < 0 and diff_y == 0:
        return -diff_x * COST_FORWARD
    if dir_y == -1 and diff_y < 0 and diff_x == 0:
        return -diff_y * COST_FORWARD
    if dir_y == 1 and diff_y > 0 and diff_x == 0:
        return diff_y * COST_FORWARD
    if abs(diff_x) > 0 and abs(diff_y) > 0:
        return (abs(diff_x) + abs(diff_y)) * COST_FORWARD + 2 * COST_ROTATE
    return (abs(diff_x) + abs(diff_y)) * COST_FORWARD + COST_ROTATE


def render(map, path):
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if (x, y) in path:
                print("X", end="")
            else:
                print(cell, end="")
        print()


def find_best_path(map, loc, orientation, goal):
    to_explore = [(loc, orientation, 0, [loc])]
    visited = {}
    visited[(loc, orientation)] = 0
    lowest_cost = float("inf")
    lowest_cost_path = None
    while to_explore:
        loc, orientation, cost, path = to_explore.pop(0)
        if loc == goal:
            if cost < lowest_cost:
                lowest_cost = cost
                lowest_cost_path = path  # noqa
            continue
        for new_loc, new_orient, move_cost in moves_to_make(loc, orientation):
            if (new_loc, new_orient) in visited and visited[
                (new_loc, new_orient)
            ] <= cost:
                continue
            visited[(new_loc, new_orient)] = cost
            new_cost = cost + move_cost
            if new_cost >= lowest_cost:
                continue

            content = map[new_loc[1]][new_loc[0]]
            if content == WALL:
                continue

            estimated_cost = heuristig_cost(new_loc, new_orient, goal)
            if new_cost + estimated_cost >= lowest_cost:
                continue

            to_explore.append((new_loc, new_orient, new_cost, path + [new_loc]))
    # render(map, lowest_cost_path)
    return lowest_cost


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    input_data_mat = [list(line) for line in input_data]

    # Part 1
    start = find(input_data_mat, START)
    end = find(input_data_mat, END)

    result1 = find_best_path(input_data_mat, start, (1, 0), end)
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    try:
        assert main("input_example.txt") == (7036, 24)
        assert main("input_example2.txt") == (11048, 24)
        assert main("input.txt") == (82460, 24)
    except AssertionError:
        print("❌ wrong")
