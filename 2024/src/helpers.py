from __future__ import annotations

from enum import Enum
import io
import functools
import fileinput
import math
import operator
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import sys

from typing import (
    List,
    Tuple,
    Any,
    Dict,
    Sequence,
    TypeVar,
    Callable,
    Iterable,
    Iterator,
    Optional,
    TextIO,
)
import numpy
import numpy.typing


# list of lines
def read_input() -> List[str]:
    return list(l.strip() for l in fileinput.input())

def read_input_slurp() -> str:
    return '\n'.join(read_input())

# list of lists of lines split by delimiter
def read_input_split(
    sep: str = " ",
    nsplit: Optional[int] = 1,
    mapper: Optional[Callable[[str], Any]] = None,
) -> List[List[Any]]:
    if nsplit is None:
        nsplit = sys.maxsize
    if mapper is None:

        def mapper(x):
            return x

    return [list(map(mapper, l.strip().split(sep, nsplit))) for l in read_input()]


# single line of separated numbers
def read_input_numbers(sep: str = ",") -> List[int]:
    l = read_input()
    assert len(l) == 1
    return [int(s) for s in l[0].split(sep)]


T = TypeVar("T", bound=numpy.generic)


def read_input_digit_grid() -> numpy.typing.NDArray[numpy.int_]:
    ret = numpy.array(
        list(list(numpy.int_(i) for i in l) for l in read_input()), dtype="i1"
    )
    ret.setflags(write=False)
    return ret


def read_input_grid() -> numpy.typing.NDArray[numpy.str_]:
    ret = numpy.array(
        list(list(numpy.str_(i) for i in l) for l in read_input()), dtype="U1"
    )
    ret.setflags(write=False)
    return ret


NumericGrid = numpy.typing.NDArray[numpy.int_]


def most_common_byte(r: NumericGrid) -> int:
    return int(numpy.sum(r == 1) >= numpy.sum(r == 0))


def neighbors(grid: NumericGrid, i: int, j: int) -> Iterable[Tuple[int, int]]:
    h, w = grid.shape
    for pos in ((i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)):
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= h or pos[1] >= w:
            continue
        yield pos


def neighbors8(grid: NumericGrid, i: int, j: int) -> Iterable[Tuple[int, int]]:
    h, w = grid.shape
    for pos in (
        (i, j + 1),
        (i, j - 1),
        (i + 1, j),
        (i - 1, j),
        (i + 1, j + 1),
        (i - 1, j - 1),
        (i + 1, j - 1),
        (i - 1, j + 1),
    ):
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= h or pos[1] >= w:
            continue
        yield pos


def neighbors9_vals(grid: NumericGrid, i: int, j: int) -> Iterator[int]:
    h, w = grid.shape
    for pos in (
        (i - 1, j - 1),
        (i - 1, j),
        (i - 1, j + 1),
        (i, j - 1),
        (i, j),
        (i, j + 1),
        (i + 1, j - 1),
        (i + 1, j),
        (i + 1, j + 1),
    ):
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= h or pos[1] >= w:
            yield 0
        else:
            yield grid[pos]


def grid_line(
    grid: NumericGrid, i: int, j: int, step: Tuple[int, int]
) -> Iterator[int]:
    h, w = grid.shape
    while True:
        i += step[0]
        j += step[1]
        if i < 0 or i >= h or j < 0 or j >= w:
            break
        yield grid[i][j]


# Goofy replacement since cmp was removed in python3 (!)
def cmp(a: int, b: int) -> int:
    return (a > b) - (a < b)


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    @staticmethod
    def from_str(s: str) -> Point:
        return Point(*map(int, s.split(",")))

    def tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def __neg__(self) -> Point:
        return Point(-self.x, -self.y)

    def __mul__(self, other: int) -> Point:
        return Point(self.x * other, self.y * other)

    def sign(self) -> Point:
        return Point(numpy.sign(self.x), numpy.sign(self.y))


def print_numpy_grid(g: numpy.typing.NDArray[T]):
    for row in g:
        print("".join(str(s) for s in row))


def print_grid(g: Dict[Point, Any]) -> None:
    min_i = min(p.x for p in g.keys())
    max_i = max(p.x for p in g.keys())
    min_j = min(p.y for p in g.keys())
    max_j = max(p.y for p in g.keys())
    for j in range(min_j, max_j + 1):
        for i in range(min_i, max_i + 1):
            print(g.get(Point(i, j), "."), end="")
        print()


def write_grid(grid: Dict[Point, int], path: str) -> None:
    import PIL.Image, PIL.ImageDraw

    img_size = 3000
    min_i = min(p.x for p in grid.keys())
    max_i = max(p.x for p in grid.keys())
    min_j = min(p.y for p in grid.keys())
    max_j = max(p.y for p in grid.keys())
    x_range, y_range = max_i - min_i, max_j - min_j
    square_range = max(x_range, y_range)
    scale = img_size / square_range
    max_fill = max(grid.values())

    img = PIL.Image.new("RGB", (img_size, img_size))
    draw = PIL.ImageDraw.Draw(img)
    for pt, count in grid.items():
        r, g, b = (count * int(255 / max_fill),) * 3
        if count == max_fill:
            print(pt, count, r)
            (r, g, b) = (255, 0, 0)
        draw.rectangle(
            (scale * pt.x, scale * pt.y, scale * (pt.x + 1), scale * (pt.y + 1)),
            fill=(r, g, b),
        )
    img.save(path)


class BitsOperator(Enum):
    SUM = 0
    PRODUCT = 1
    MIN = 2
    MAX = 3
    LITERAL = 4
    GT = 5
    LT = 6
    EQ = 7


def prod(args: List[int]) -> int:
    return functools.reduce(operator.mul, args)


def eq(args: List[int]) -> int:
    return functools.reduce(operator.eq, args)


def lt(args: List[int]) -> int:
    return functools.reduce(operator.lt, args)


def gt(args: List[int]) -> int:
    return functools.reduce(operator.gt, args)


def fail(args: List[int]) -> int:
    return 0


opmap: List[Callable[[List[int]], int]] = [sum, prod, min, max, fail, gt, lt, eq]


@dataclass
class BitsPacket:
    version: int
    type_id: BitsOperator
    children: List[BitsPacket]
    literal_value: Optional[int]

    def __init__(self, version: int, type_id: int):
        self.version = version
        self.type_id = BitsOperator(type_id)
        self.children = []
        self.literal_value = None

    def eval(self) -> int:
        if self.type_id == BitsOperator.LITERAL:
            assert self.literal_value is not None
            return self.literal_value
        else:
            results = [c.eval() for c in self.children]
            return opmap[self.type_id.value](results)

    def print(self, indent: str = "") -> None:
        if self.type_id == BitsOperator.LITERAL:
            print(
                f"{indent}BitsPacket(ver={self.version}, type-{self.type_id}, val={self.literal_value})"
            )
        else:
            print(f"{indent}BitsPacket(ver={self.version}, type-{self.type_id})")
            for c in self.children:
                c.print(indent + "  ")


def decode_packet(p: TextIO) -> BitsPacket:
    ver, type_id = int(p.read(3), 2), int(p.read(3), 2)
    print("decode ver", ver, "type", type_id, p)

    packet = BitsPacket(ver, type_id)

    sub_value = None
    if type_id == 4:
        s = ""
        while p.read(1) != "0":
            nib = p.read(4)
            s += nib
        s += p.read(4)
        literal = int(s, 2)
        print("literal", s, literal)
        sub_value = literal
        packet.literal_value = literal
    else:
        length_type_id = p.read(1)
        print(type_id)
        print("op is", type_id)
        if length_type_id == "0":
            nib = p.read(15)
            total_length = int(nib, 2)
            print("subpacket length", total_length)
            p = io.StringIO(p.read(total_length))
            acc = []
            while p.tell() < total_length:
                val = decode_packet(p)
                acc.append(val)
            packet.children = acc
        else:
            nib = p.read(11)
            num_subs = int(nib, 2)
            print("subpacket group", num_subs)
            acc = []
            for i in range(num_subs):
                val = decode_packet(p)
                acc.append(val)
            packet.children = acc
    return packet


@dataclass(frozen=True)
class Coordinate:
    row: int
    col: int

    def __add__(self, other: 'Coordinate') -> 'Coordinate':
        return Coordinate(self.row + other.row, self.col + other.col)

    def __sub__(self, other: 'Coordinate') -> 'Coordinate':
        return Coordinate(self.row - other.row, self.col - other.col)

    def __neg__(self) -> 'Coordinate':
        return Coordinate(-self.row, -self.col)

    def __mul__(self, x):
        return Coordinate(x * self.row, x * self.col)

    def __iter__(self):
        yield self.row
        yield self.col


up = Coordinate(-1, 0)
down = Coordinate(1, 0)
left = Coordinate(0, -1)
right = Coordinate(0, 1)
up_left = up + left
down_left = down + left
up_right = up + right
down_right = down + right

DIRECTIONS = [up, down, left, right, up_left, up_right, down_left, down_right]

class GridBase(ABC):
    @abstractmethod
    def __getitem__(self, idx: Any) -> str:
        pass

    @abstractmethod
    def __setitem__(self, idx: Any, val: str):
        pass

    @abstractmethod
    def in_bounds(self, coord: Coordinate) -> bool:
        pass

    @abstractmethod
    def items(self) -> Iterator[Tuple[Coordinate, str]]:
        pass

    @abstractmethod
    def __init__(self):
        # So that derived classes remember to init
        pass

    def get(self, coord: Coordinate, default: Optional[str] = None) -> Optional[str]:
        # Common implementation: try __getitem__, catch exceptions
        try:
            return self[coord]
        except (IndexError, KeyError):
            return default

    def neighbors(self, row: int, col: int) -> Iterator[Coordinate]:
        # Common implementation using directions and in_bounds
        for d in DIRECTIONS:
            n = Coordinate(row + d.row, col + d.col)
            if self.in_bounds(n):
                yield n

    def neighbors4(self, pos: Coordinate) -> Iterator[Coordinate]:
        # Common implementation using directions and in_bounds
        for d in (up, down, left, right):
            n = pos + d
            if self.in_bounds(n):
                yield n

    def find_all(self, val: str) -> List[Coordinate]:
        return [coord for coord, cell in self.items() if cell == val]

    def contains(self, val: str) -> bool:
        return any(cell == val for _, cell in self.items())

    def bulk_set(self, coords_values: List[Tuple[Coordinate, str]]):
        for coord, v in coords_values:
            self[coord] = v

    def apply(self, func):
        # Make a list so we don't mutate while iterating
        for coord, val in list(self.items()):
            self[coord] = func(coord, val)

    def print(self):
        # Default printing just prints items in no specific layout
        for coord, val in self.items():
            print(f"{coord}: {val}")

@dataclass
class Grid(GridBase):
    nrows: int = 0
    ncols: int = 0
    entries: List[List[str]] = field(default_factory=list)

    @classmethod
    def from_list_of_strings(cls, rows: List[str]) -> 'Grid':
        g = cls()
        g.entries = [list(r) for r in rows]
        g.nrows = len(g.entries)
        g.ncols = len(g.entries[0]) if g.nrows > 0 else 0
        return g

    def __getitem__(self, idx):
        if isinstance(idx, Coordinate):
            r, c = idx.row, idx.col
        else:
            r, c = idx
        if r < 0 or c < 0 or r >= self.nrows or c >= self.ncols:
            raise IndexError("Index out of bounds")
        return self.entries[r][c]

    def __setitem__(self, idx, val):
        if isinstance(idx, Coordinate):
            r, c = idx.row, idx.col
        else:
            r, c = idx
        if r < 0 or c < 0 or r >= self.nrows or c >= self.ncols:
            raise IndexError("Index out of bounds")
        self.entries[r][c] = val

    def in_bounds(self, coord: Coordinate) -> bool:
        return 0 <= coord.row < self.nrows and 0 <= coord.col < self.ncols

    def items(self) -> Iterator[Tuple[Coordinate, str]]:
        for r in range(self.nrows):
            for c in range(self.ncols):
                yield Coordinate(r, c), self.entries[r][c]

    def print(self):
        print('\n'.join(''.join(row) for row in self.entries))

    # Extra methods that only make sense for bounded grids
    def row_values(self, r: int) -> List[str]:
        if r < 0 or r >= self.nrows:
            raise IndexError("Row out of range")
        return self.entries[r]

    def column_values(self, c: int) -> List[str]:
        if c < 0 or c >= self.ncols:
            raise IndexError("Column out of range")
        return [self.entries[r][c] for r in range(self.nrows)]

    def walk_edges(self):
        for r in range(self.nrows):
            yield Coordinate(r, 0)
            yield Coordinate(r, self.ncols - 1)
        for c in range(self.ncols):
            yield Coordinate(0, c)
            yield Coordinate(self.nrows - 1, c)

@dataclass
class SparseGrid(GridBase):
    def __init__(self, default: Optional[str] = None):
        self.cells: Dict[Tuple[int,int], str] = {}
        self.default = default

    def __getitem__(self, idx):
        if isinstance(idx, Coordinate):
            r, c = idx.row, idx.col
        else:
            r, c = idx
        if (r, c) in self.cells:
            return self.cells[(r, c)]
        if self.default is not None:
            return self.default
        # Not found: treat as KeyError so get() can handle it
        raise KeyError("Cell not found")

    def __setitem__(self, idx, val):
        if isinstance(idx, Coordinate):
            r, c = idx.row, idx.col
        else:
            r, c = idx
        self.cells[(r, c)] = val

    def in_bounds(self, coord: Coordinate) -> bool:
        # For sparse, infinite space assumed, always True
        return True

    def items(self) -> Iterator[Tuple[Coordinate, str]]:
        for (r,c), val in self.cells.items():
            yield Coordinate(r,c), val

def to_sparse(grid: Grid) -> SparseGrid:
    sg = SparseGrid()
    for coord, val in grid.items():
        sg[coord] = val
    return sg

def to_dense(sparse: SparseGrid, top_left: Coordinate, bottom_right: Coordinate) -> Grid:
    rows = bottom_right.row - top_left.row + 1
    cols = bottom_right.col - top_left.col + 1
    arr = []
    for r in range(top_left.row, top_left.row + rows):
        row_arr = []
        for c in range(top_left.col, top_left.col + cols):
            val = sparse.get(Coordinate(r, c), default=' ')
            row_arr.append(val)
        arr.append(row_arr)

    g = Grid()
    g.entries = arr
    g.nrows = rows
    g.ncols = cols
    return g
