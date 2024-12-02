import itertools
import math
import os
import re
from collections import defaultdict

this_folder = "\\".join(__file__.split("\\")[:-1])


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    input_data_mat = [[int(x) for x in line.split()] for line in input_data]

    # Part 1
    save_reports = 0
    for report in input_data_mat:
        diffs = [x - y for x, y in zip(report[:-1], report[1:])]
        abs_diffs = [abs(x) for x in diffs]
        _max, _min = max(diffs), min(diffs)
        abs_max, abs_min = max(abs_diffs), min(abs_diffs)

        if _max * _min < 0:
            continue
        if abs_min == 0:
            continue
        if abs_max > 3:
            continue
        save_reports += 1
    result1 = save_reports
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    save_reports = 0
    for report in input_data_mat:
        for drop_loc in [None] + list(range(len(report))):
            report_copy = report.copy()
            if drop_loc is not None:
                report_copy.pop(drop_loc)
            diffs = [x - y for x, y in zip(report_copy[:-1], report_copy[1:])]
            abs_diffs = [abs(x) for x in diffs]
            _max, _min = max(diffs), min(diffs)
            abs_max, abs_min = max(abs_diffs), min(abs_diffs)

            if _max * _min < 0:
                continue
            if abs_min == 0:
                continue
            if abs_max > 3:
                continue
            save_reports += 1
            break
    result2 = save_reports
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    try:
        assert main("input_example.txt") == (2, 4)
        assert main("input.txt") == (252, 324)
    # assert main("input2.txt") == (42, 24)
    except AssertionError as e:
        print("❌ not correct")
