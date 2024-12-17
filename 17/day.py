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


def run_program(program, reg_A, reg_B, reg_C) -> str:
    instruction_pointer = 0
    output = []
    while True:
        if instruction_pointer >= len(program):
            break
        opcode = program[instruction_pointer]
        instruction = opcode_to_instruction[opcode]
        literal_operand = program[instruction_pointer + 1]
        combo_operand = literal_to_combo(literal_operand, reg_A, reg_B, reg_C)

        if instruction == "adv":
            reg_A = int(reg_A / 2**combo_operand)
        elif instruction == "bxl":
            # bitwise XOR
            reg_B = reg_B ^ literal_operand
        elif instruction == "bst":
            reg_B = combo_operand % 8
        elif instruction == "jnz":
            if reg_A != 0:
                instruction_pointer = literal_operand
                continue
        elif instruction == "bxc":
            reg_B = reg_B ^ reg_C
        elif instruction == "out":
            output.append(combo_operand % 8)
        elif instruction == "bdv":
            reg_B = int(reg_A / 2**combo_operand)
        elif instruction == "cdv":
            reg_C = int(reg_A / 2**combo_operand)

        instruction_pointer += 2

    return ",".join(map(str, output)), reg_A, reg_B, reg_C


def main(filename, return_all=False):
    input_data = open(f"{this_folder}/{filename}", "r").read()
    # get first three numbers
    reg_A, reg_B, reg_C, *program = map(int, re.findall(r"\d+", input_data))

    # Part 1
    result1_commas, reg_A, reg_B, reg_C = run_program(program, reg_A, reg_B, reg_C)
    print(f"Part 1 {filename}: ", result1_commas)
    if return_all:
        return result1_commas, reg_A, reg_B, reg_C
    return result1_commas


if __name__ == "__main__":
    try:
        assert main("input_example.txt") == "4,6,3,5,6,3,5,2,1,0"
        assert main("input_example2.txt", return_all=True) == ("", 0, 1, 9)
        assert main("input_example3.txt", return_all=True) == ("0,1,2", 10, 0, 0)
        assert main("input_example4.txt", return_all=True) == (
            "4,2,5,6,7,7,7,7,3,1,0",
            0,
            0,
            0,
        )
        assert main("input_example5.txt", return_all=True) == ("", 0, 26, 0)
        assert main("input_example6.txt", return_all=True) == ("", 0, 44354, 43690)
        assert main("input_example7.txt") == "0,3,5,4,3,0"
        assert main("input.txt") == "5,0,3,5,7,6,1,5,4"
    except AssertionError:
        print("❌ wrong")
