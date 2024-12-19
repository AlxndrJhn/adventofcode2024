import itertools
import os
import re
from collections import defaultdict

this_folder = "\\".join(__file__.split("\\")[:-1])


opcode_to_instruction = {
    0: "adv",
    1: "bxl",
    2: "bst",
    3: "jnz",
    4: "bxc",
    5: "out",
    6: "bdv",
    7: "cdv",
}


def literal_to_combo(literal, reg_A, reg_B, reg_C):
    if literal <= 3:
        return literal
    if literal == 4:
        return reg_A
    if literal == 5:
        return reg_B
    if literal == 6:
        return reg_C
    return None


def reverse_combo(literal, value, reg_A, reg_B, reg_C):
    if literal == 4:
        reg_A += value
    if literal == 5:
        reg_B += value
    if literal == 6:
        reg_C += value
    return reg_A, reg_B, reg_C


def reverse_one_step(program, instruction_pointer, reg_A, reg_B, reg_C, output):
    opcode = program[instruction_pointer]
    instruction = opcode_to_instruction[opcode]
    literal_operand = program[instruction_pointer + 1]
    combo_operand = literal_to_combo(literal_operand, reg_A, reg_B, reg_C)

    if instruction == "adv":
        reg_A = reg_A * 2**combo_operand
    elif instruction == "bxl":
        reg_B = reg_B ^ literal_operand
    elif instruction == "bst":
        reg_B = combo_operand % 8
    elif instruction == "jnz":
        if reg_A != 0:
            instruction_pointer = literal_operand
            return reg_A, reg_B, reg_C, instruction_pointer
    elif instruction == "bxc":
        reg_B = reg_B ^ reg_C
    elif instruction == "out":
        last_output = output.pop()
        reg_A, reg_B, reg_C = reverse_combo(
            literal_operand, last_output, reg_A, reg_B, reg_C
        )
    elif instruction == "bdv":
        reg_B = int(reg_A / 2**combo_operand)
    elif instruction == "cdv":
        reg_C = int(reg_A / 2**combo_operand)
    return reg_A, reg_B, reg_C, instruction_pointer - 2


def run_one_step(program, instruction_pointer, reg_A, reg_B, reg_C, output):
    opcode = program[instruction_pointer]
    instruction = opcode_to_instruction[opcode]
    literal_operand = program[instruction_pointer + 1]
    combo_operand = literal_to_combo(literal_operand, reg_A, reg_B, reg_C)

    if instruction == "adv":
        reg_A = int(reg_A / 2**combo_operand)
    elif instruction == "bxl":
        reg_B = reg_B ^ literal_operand
    elif instruction == "bst":
        reg_B = combo_operand % 8
    elif instruction == "jnz":
        if reg_A != 0:
            instruction_pointer = literal_operand
            return reg_A, reg_B, reg_C, instruction_pointer
    elif instruction == "bxc":
        reg_B = reg_B ^ reg_C
    elif instruction == "out":
        to_out = combo_operand % 8
        output.append(to_out)
    elif instruction == "bdv":
        reg_B = int(reg_A / 2**combo_operand)
    elif instruction == "cdv":
        reg_C = int(reg_A / 2**combo_operand)
    return reg_A, reg_B, reg_C, instruction_pointer + 2


def run_program(program, reg_A, reg_B, reg_C) -> list[int]:
    instruction_pointer = 0
    output = []
    while True:
        if instruction_pointer >= len(program):
            break
        reg_A, reg_B, reg_C, instruction_pointer = run_one_step(
            program, instruction_pointer, reg_A, reg_B, reg_C, output
        )

    return output, reg_A, reg_B, reg_C


def part1(filename, return_all=False):
    input_data = open(f"{this_folder}/{filename}", "r").read()
    reg_A, reg_B, reg_C, *program = map(int, re.findall(r"\d+", input_data))
    result1, reg_A, reg_B, reg_C = run_program(program, reg_A, reg_B, reg_C)
    result1_commas = ",".join(map(str, result1))
    print(f"Part 1 {filename}: ", result1_commas)
    if return_all:
        return result1_commas, reg_A, reg_B, reg_C
    return result1_commas


def part2(filename):
    print(f"Starting part 2 {filename}")
    input_data = open(f"{this_folder}/{filename}", "r").read()
    _, _, _, *program = map(int, re.findall(r"\d+", input_data))

    instruction_pointer = len(program) - 4
    reg_A, reg_B, reg_C = 0, 0, 0
    output = program.copy()
    output.pop()
    while True:
        reg_A, reg_B, reg_C, instruction_pointer = reverse_one_step(
            program, instruction_pointer, reg_A, reg_B, reg_C, output=output
        )
        if instruction_pointer < 0 and len(output) == 0:
            break
        if instruction_pointer < 0:
            instruction_pointer = len(program) - 4
    result2 = reg_A
    print(f"Part 2 {filename}: ", result2)
    return result2


if __name__ == "__main__":
    try:
        assert part1("input_example.txt") == "4,6,3,5,6,3,5,2,1,0"
        assert part1("input_example2.txt", return_all=True) == ("", 0, 1, 9)
        assert part1("input_example3.txt", return_all=True) == ("0,1,2", 10, 0, 0)
        assert part1("input_example4.txt", return_all=True) == (
            "4,2,5,6,7,7,7,7,3,1,0",
            0,
            0,
            0,
        )
        assert part1("input_example5.txt", return_all=True) == ("", 0, 26, 0)
        assert part1("input_example6.txt", return_all=True) == ("", 0, 44354, 43690)
        assert part1("input_example7.txt") == "0,3,5,4,3,0"
        assert part1("input.txt") == "5,0,3,5,7,6,1,5,4"

        assert part2("input_example8.txt") == 117440
        # assert part2("input.txt") == 1
    except AssertionError:
        print("❌ wrong")
