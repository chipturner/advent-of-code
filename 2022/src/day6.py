import helpers

import itertools
import collections


def main() -> None:
    lines = helpers.read_input()
    print(lines)
    pkt = lines[0]
    chunks = list(pkt[n:n+4] for n in range(len(pkt) - 4))
    for idx, chunk in enumerate(chunks):
        if len(set(chunk)) == 4:
            print(chunk, idx + 4)


main()
