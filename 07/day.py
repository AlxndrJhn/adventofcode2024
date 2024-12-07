import itertools
import math
import os
import re
from collections import defaultdict

this_folder = "\\".join(__file__.split("\\")[:-1])


def evaluate(operations, operators):
    result = operators[0]
    for operation, operator in zip(operations, operators[1:]):
        result = operation([result, operator])
    return result


def could_be_true(total, operators, ALLOWED_OPERATIONS, operations):
    if len(operations) == len(operators) - 1:
        return evaluate(operations, operators) == total
    for operation in ALLOWED_OPERATIONS:
        if could_be_true(
            total, operators, ALLOWED_OPERATIONS, operations + [operation]
        ):
            return True
    return False


def main(filename):
    cal_equations_str = open(f"{this_folder}/{filename}", "r").read().split("\n")
    cal_equations = []
    for cal_equation_str in cal_equations_str:
        parts = cal_equation_str.split(": ")
        total = int(parts[0])
        operators = [int(x) for x in parts[1].split(" ")]
        cal_equations.append((total, operators))

    # Part 1
    ALLOWED_OPERATIONS = [math.prod, sum]
    result1 = 0
    for total, operators in cal_equations:
        if could_be_true(total, operators, ALLOWED_OPERATIONS, []):
            result1 += total
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 0
    ALLOWED_OPERATIONS = [math.prod, sum, lambda x: int(str(x[0]) + str(x[1]))]
    for total, operators in cal_equations:
        if could_be_true(total, operators, ALLOWED_OPERATIONS, []):
            result2 += total
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    assert main("input_example.txt") == (3749, 11387)
    assert main("input.txt") == (267566105056, 116094961956019)
