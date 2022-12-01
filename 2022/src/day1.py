import fileinput
import itertools
import collections
import sys

def main() -> None:
    lines = [ [ int(v) for v in l.split('\n') ] for l in sys.stdin.read().strip().split('\n\n') ]
    sums = [ sum(e) for e in lines ]
    sums.sort(reverse=True)
    print(sum(sums[:3]))


main()
