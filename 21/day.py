from collections import defaultdict
from itertools import permutations

this_folder = "\\".join(__file__.split("\\")[:-1])

# this solution is copied from https://github.com/sanvirk99/adventcode/blob/main/day21recursion.py

numPad = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["#", "0", "A"]]

dirPad = [["#", "^", "A"], ["<", "v", ">"]]

moveSpace = []
for i in range(-3, 4):
    for j in range(-2, 3):
        if abs(i) in range(0, 4) and abs(j) in range(0, 3):
            moveSpace.append((i, j))

dirSpace = []
for i in range(-1, 2):
    for j in range(-2, 3):
        if abs(i) in range(0, 2) and abs(j) in range(0, 3):
            dirSpace.append((i, j))


def symbolx(x):
    if x < 0:
        return "^" * abs(x)
    if x > 0:
        return "v" * abs(x)
    return ""


def symboly(y):
    if y < 0:
        return "<" * abs(y)
    if y > 0:
        return ">" * abs(y)
    return ""


directions = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}


def validate(grid, cur, end, seq):
    def dfs(cur, i):
        x, y = cur
        if cur == end:
            return True
        if grid[x][y] == "#":
            return False
        dx, dy = directions[seq[i]]
        return dfs((x + dx, y + dy), i + 1)

    return dfs(cur, 0)


numMoves = defaultdict(lambda: defaultdict())
for i in range(len(numPad)):
    for j in range(len(numPad[0])):
        if numPad[i][j] == "#":
            continue
        for move in moveSpace:
            dx, dy = move
            nx, ny = i + dx, j + dy
            if (
                nx in range(len(numPad))
                and ny in range(len(numPad[0]))
                and numPad[nx][ny] != "#"
            ):
                seq1 = symbolx(dx) + symboly(dy)
                perm = list(permutations(seq1))
                unique = set()
                for p in perm:
                    if validate(numPad, (i, j), (nx, ny), "".join(p)):
                        temp = list(p)
                        temp.append("A")
                        unique.add("".join(temp))
                numMoves[numPad[i][j]][numPad[nx][ny]] = unique

dirMoves = defaultdict(lambda: {})
for i in range(len(dirPad)):
    for j in range(len(dirPad[0])):
        if dirPad[i][j] == "#":
            continue
        for move in dirSpace:
            dx, dy = move
            nx, ny = i + dx, j + dy
            if (
                nx in range(len(dirPad))
                and ny in range(len(dirPad[0]))
                and dirPad[nx][ny] != "#"
            ):
                seq1 = symbolx(dx) + symboly(dy)
                perm = list(permutations(seq1))
                unique = set()
                for p in perm:
                    if validate(dirPad, (i, j), (nx, ny), "".join(p)):
                        temp = list(p)
                        if not temp:
                            temp = ["A"]
                        else:
                            temp.append("A")
                        unique.add("".join(temp))

                dirMoves[dirPad[i][j]][dirPad[nx][ny]] = unique


def allcombination(totype):
    res = []

    def dfs(totype, combo, from_):
        if len(totype) == 0:
            res.append(combo)
            return
        for move in numMoves[from_][totype[0]]:
            choice = combo + move
            dfs(totype[1:], choice, totype[0])

    dfs(totype, "", "A")
    return res


def dircombinations(totype):
    res = []

    def dfs(totype, combo, from_):
        if len(totype) == 0:
            res.append(combo)
            return
        for move in dirMoves[from_][totype[0]]:
            choice = combo + move
            dfs(totype[1:], choice, totype[0])

    dfs(totype, "", "A")
    return res


def chainRobot(letter, prev, end, seqstart):
    mem = {}

    def dfs(letter, prev, i, start):
        if i == end:
            return 1
        if (letter, prev, i, start) in mem:
            return mem[(letter, prev, i, start)]
        mincount = float("inf")
        if start:
            prev = "A"
        for index, move in enumerate(dirMoves[prev][letter]):
            count = 0
            cur = prev
            begin = True
            for each in move:
                count += dfs(each, cur, i + 1, begin)
                begin = False
                cur = each
            if count < mincount:
                mincount = min(mincount, count)
        mem[(letter, prev, i, start)] = mincount
        return mincount

    return dfs(letter, prev, 0, seqstart)


def type(totype, depth):
    combinations = allcombination(totype)
    minlen = float("inf")
    for seq in combinations:
        prev = "A"
        start = True
        res = 0
        for letter in seq:
            res += chainRobot(letter, prev, depth, start)
            start = False
            prev = letter
        minlen = min(res, minlen)
    return minlen * int(totype[:-1])


def part1(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().strip().split("\n")

    result1 = 0
    for line in input_data:
        result1 += type(line, depth=2)
    print(f"Part 1 {filename}: ", result1)
    return result1


def part2(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().strip().split("\n")

    result2 = 0
    for line in input_data:
        result2 += type(line, depth=25)
    print(f"Part 2 {filename}: ", result2)
    return result2


if __name__ == "__main__":
    try:
        assert part1("input_example.txt") == 68 * 29
        assert part1("input.txt") == 156714
        assert part2("input_example.txt") == 2379451789590
        assert part2("input.txt") == 191139369248202
    except AssertionError:
        print("❌ wrong")
