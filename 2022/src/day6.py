import helpers
import more_itertools


def main() -> None:
    lines = helpers.read_input()
    print(lines)
    pkt = lines[0]
    for idx, chunk in enumerate(more_itertools.windowed(pkt, 14)):
        if len(set(chunk)) == 14:
            print(chunk, idx + 14)


main()
