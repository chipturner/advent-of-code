import pprint
import helpers

import itertools
import collections

input = r"""
            L   M           M     
        D   R   Z           C   L 
        C   S   T   G       V   M 
R       L   Q   B   B       D   F 
H   B   G   D   Q   Z       T   J 
M   J   H   M   P   S   V   L   N 
P   C   N   T   S   F   R   G   Q 
Z   P   S   F   F   T   N   P   W 
"""


def main() -> None:
    data = []
    for i in range(9):
        data.append([])
        for idx, l in enumerate(input.lstrip('\n').splitlines()):
            ch = l[i * 4]
            if ch != ' ':
                data[-1].append(ch)
        data[-1].reverse()
    print(data)

    lines = helpers.read_input()
    for line in lines:
        cmds = line.split()
        if not cmds or cmds[0] != 'move':
            continue
        n, f, t = int(cmds[1]), int(cmds[3]) - 1, int(cmds[5]) - 1
        print(n, f, t)
        for i in range(n):
            ch = data[f].pop()
            data[t].append(ch)
    pprint.pprint(data)
    print(''.join(data[i][-1] for i in range(9)))
            
    
main()
