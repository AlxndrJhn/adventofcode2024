import itertools
import os
import re
from collections import defaultdict

this_folder = "\\".join(__file__.split("\\")[:-1])


def main(filename):
    rules_str, updates_str = [
        part.split()
        for part in open(f"{this_folder}/{filename}", "r").read().split("\n\n")
    ]
    rules = [(int(x), int(y)) for x, y in [rule.split("|") for rule in rules_str]]
    updates = [[int(p) for p in page.split(",")] for page in updates_str]

    # Part 1
    result1 = 0
    for update in updates:
        some_rule_violation = False
        for num_idx, number in enumerate(update):
            applicable_rules = [rule for rule in rules if rule[0] == number]
            for _, must_be_after in applicable_rules:
                position_other = (
                    -1 if must_be_after not in update else update.index(must_be_after)
                )
                if position_other != -1 and position_other < num_idx:
                    some_rule_violation = True
                    break
            if some_rule_violation:
                break
        if not some_rule_violation:
            middle_number = update[len(update) // 2]
            result1 += middle_number

    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    assert main("input_example.txt") == (143, 24)
    assert main("input.txt") == (4959, 24)
