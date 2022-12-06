import helpers

import itertools
import collections


def main() -> None:
    lines = helpers.read_input()
    print(lines)
    pkt = lines[0]
    chunks = list(pkt[n:n+14] for n in range(len(pkt) - 14))
    for idx, chunk in enumerate(chunks):
        if len(set(chunk)) == 14:
            print(chunk, idx + 14)


main()
