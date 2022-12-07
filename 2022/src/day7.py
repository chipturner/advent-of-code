import helpers

import itertools
import collections

from dataclasses import dataclass

@dataclass
class Dir:
    def __init__(self, name):
        self.children = []
        self.files = []
        self.size = 0
        self.name = name
        self.parent = None

    def __str__(self):
        return f"Dir({self.name}, tot={self.size})"

    def nice_print(self, indent=0):
        padding = '  ' * indent
        print(f'{padding}Dir({self.name}, tot={self.size})')
        for f in self.files:
            print(f'{padding} {f}')
        for c in self.children:
            c.nice_print(indent + 2)

    def calc_size(self):
        size = 0
        for f in self.files:
            size += f[0]
        for d in self.children:
            d.calc_size()
            size += d.size
        self.size = size

    def walk(self):
        yield self
        for d in self.children:
            for c in d.walk():
                yield c

def main() -> None:
    lines = helpers.read_input()
    dirs = {}
    root = Dir('/')
    dirs['/'] = root

    cwd = root
    while lines:
        cmd = lines.pop(0).split()
        if cmd[0] == '$':
            if cmd[1] == 'cd':
                if cmd[2] == '/':
                    cwd = root
                elif cmd[2] == '..':
                    cwd = cwd.parent
                else:
                    print(cmd, cwd)
                    cwd = list(d for d in cwd.children if d.name == cmd[2])[0]
            elif cmd[1] == 'ls':
                contents = []
                while lines and lines[0][0] != '$':
                    entry = lines.pop(0).split()
                    print(entry)
                    if entry[0] == 'dir':
                        newdir = Dir(entry[1])
                        newdir.parent = cwd
                        cwd.children.append(newdir)
                    else:
                        cwd.files.append((int(entry[0]), entry[1]))
    root.calc_size()
    root.nice_print()
    qual_size = 0
    for c in root.walk():
        if c.size <= 100000:
            print(c)
            qual_size += c.size
    print(qual_size)

    total = 70000000
    need  = 30000000
    unused = total - root.size

    choices = []
    for c in root.walk():
        print('qq', unused + c.size, need, c)
        if unused + c.size >= need:
            choices.append(c)
    print(choices)
    choices.sort(key=lambda d: d.size)
    print(choices[0])

main()
