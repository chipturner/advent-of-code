from __future__ import annotations

import helpers

from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Iterator


@dataclass
class Dir:
    name: str
    children: List[Dir] = field(default_factory=list, repr=False)
    files: List[Tuple[int, str]] = field(default_factory=list, repr=False)
    parent: Optional[Dir] = field(default=None, repr=False)

    def nice_print(self, indent: int = 0) -> None:
        padding = "  " * indent
        print(f"{padding}{self}")
        for f in self.files:
            print(f"  {padding}{f}")
        for c in self.children:
            c.nice_print(indent + 1)

    def size(self) -> int:
        size = sum(f[0] for f in self.files)
        for c in self.children:
            size += c.size()
        return size

    def walk(self) -> Iterator[Dir]:
        yield self
        for d in self.children:
            for c in d.walk():
                yield c


def main() -> None:
    lines = helpers.read_input()
    dirs = {}
    root = Dir("/")
    dirs["/"] = root

    cwd = root
    while lines:
        cmd = lines.pop(0).split()
        if cmd[0] == "$":
            if cmd[1] == "cd":
                if cmd[2] == "/":
                    cwd = root
                elif cmd[2] == "..":
                    assert cwd.parent is not None
                    cwd = cwd.parent
                else:
                    cwd = list(d for d in cwd.children if d.name == cmd[2])[0]
            elif cmd[1] == "ls":
                while lines and lines[0][0] != "$":
                    entry = lines.pop(0).split()
                    if entry[0] == "dir":
                        newdir = Dir(entry[1])
                        newdir.parent = cwd
                        cwd.children.append(newdir)
                    else:
                        cwd.files.append((int(entry[0]), entry[1]))
    root.nice_print()
    qual_size = 0
    for c in root.walk():
        if c.size() <= 100000:
            print(c)
            qual_size += c.size()
    print(qual_size)

    total = 70000000
    need = 30000000
    unused = total - root.size()

    choices = []
    for c in root.walk():
        if unused + c.size() >= need:
            choices.append(c)
    print(choices)
    choices.sort(key=lambda d: d.size())
    print(choices[0])


main()
