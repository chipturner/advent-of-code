from __future__ import annotations

import helpers

import itertools
import collections


def main() -> None:
    lines_orig = helpers.read_input()

    for i in range(20):
        d = dict()
        lines = lines_orig.copy()
        while lines:
            line = lines.pop(0)
            line = line.replace(':', '=')
            if line.startswith('root='):
                line = line.replace('+', '==')
            try:
                exec(line, None, d)
                #print(d)
            except Exception as e:
                lines.append(line)
                #print(e)
        print(d)
        
            

main()
