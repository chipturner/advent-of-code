import sys


def parse_input():
    lines = sys.stdin.read()
    column_lines, moves = lines.split("\n\n")
    return column_lines.strip("\n").split("\n"), moves.rstrip("\n").split("\n")


def main() -> None:
    column_lines, moves = parse_input()
    column_count = (len(column_lines[-1]) + 1) // 4

    data = []
    for i in range(column_count):
        data.append([])
        for line in column_lines:
            ch = line[i * 4 + 1]
            if ch != " ":
                data[-1].append(ch)
        data[-1].reverse()

    for move in moves:
        cmds = move.split()
        assert cmds[0] == "move"
        n, f, t = int(cmds[1]), int(cmds[3]) - 1, int(cmds[5]) - 1
        chunk = data[f][-n:]
        data[f][-n:] = []
        data[t].extend(chunk)
    print("".join(data[i][-1] for i in range(column_count)))


main()
