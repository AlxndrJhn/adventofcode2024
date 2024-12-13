import math
import re


this_folder = "\\".join(__file__.split("\\")[:-1])


def get_numbers(button):
    pattern = r"(-?\d+)"
    return tuple(map(int, re.findall(pattern, button)))


A_COST = 3
B_COST = 1
MAX_PUSHES = 100


def solver(a_button, b_button, prize_loc):
    a = a_button[0]
    b = a_button[1]
    c = b_button[0]
    d = b_button[1]
    p1 = prize_loc[0]
    p2 = prize_loc[1]

    determinant = a * d - b * c
    s1 = (d * p1 - c * p2) / determinant
    s2 = (-b * p1 + a * p2) / determinant
    solution = [s1, s2]
    all_vals_are_int = all([val == int(val) for val in solution])
    if all_vals_are_int:
        return A_COST * s1 + B_COST * s2, solution
    return math.inf, solution


def main(filename):
    device_infos = open(f"{this_folder}/{filename}", "r").read().split("\n\n")
    device_ab_prizes = []
    for device_info in device_infos:
        device_ab_prizes.append([get_numbers(part) for part in device_info.split("\n")])
    # Part 1
    result1 = 0
    for button_a, button_b, prize_loc in device_ab_prizes:
        lowest_solution, _ = solver(button_a, button_b, prize_loc)
        if lowest_solution != math.inf:
            result1 += lowest_solution
    print(f"Part 1 {filename}: ", int(result1))

    # Part 2
    result2 = 0
    PRICE_OFFSET = 10000000000000
    for button_a, button_b, prize_loc in device_ab_prizes:
        prize_loc = (prize_loc[0] + PRICE_OFFSET, prize_loc[1] + PRICE_OFFSET)
        lowest_solution, _ = solver(button_a, button_b, prize_loc)
        if lowest_solution != math.inf:
            result2 += lowest_solution
    print(f"Part 2 {filename}: ", int(result2))
    return result1, result2


if __name__ == "__main__":
    try:
        assert main("input_example.txt") == (480, 875318608908)
        assert main("input.txt") == (26299, 107824497933339)
    except AssertionError:
        print("❌ wrong")
