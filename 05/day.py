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
    incorrect_updates = []
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
                    incorrect_updates.append(update)
                    break
            if some_rule_violation:
                break
        if not some_rule_violation:
            middle_number = update[len(update) // 2]
            result1 += middle_number

    print(f"Part 1 {filename}: ", result1)

    # Part 2

    def get_violated_rules(update):
        rules_violated = set()
        for num_idx, number in enumerate(update):
            applicable_rules = [rule for rule in rules if rule[0] == number]
            for must_be_before, must_be_after in applicable_rules:
                position_other = (
                    -1 if must_be_after not in update else update.index(must_be_after)
                )
                if position_other != -1 and position_other < num_idx:
                    rules_violated.add((must_be_before, must_be_after))
        return rules_violated

    result2 = 0
    for update in incorrect_updates:
        while len(get_violated_rules(update)):
            must_be_before, must_be_after = list(get_violated_rules(update))[0]
            idx1 = update.index(must_be_before)
            idx2 = update.index(must_be_after)
            update[idx1], update[idx2] = update[idx2], update[idx1]
        middle_number = update[len(update) // 2]
        result2 += middle_number
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    assert main("input_example.txt") == (143, 123)
    assert main("input.txt") == (4959, 4655)
