import unittest
from helpers import *

class TestCoordinate(unittest.TestCase):
    def test_addition(self):
        a = Coordinate(2, 3)
        b = Coordinate(-1, 4)
        self.assertEqual(a + b, Coordinate(1, 7))

    def test_subtraction(self):
        a = Coordinate(2, 3)
        b = Coordinate(1, 1)
        self.assertEqual(a - b, Coordinate(1, 2))

    def test_negation(self):
        a = Coordinate(2, -3)
        self.assertEqual(-a, Coordinate(-2, 3))


class TestGrid(unittest.TestCase):
    def setUp(self):
        self.grid = Grid.from_list_of_strings([
            "abcd",
            "efgh",
            "ijkl",
        ])

    def test_dimensions(self):
        self.assertEqual(self.grid.nrows, 3)
        self.assertEqual(self.grid.ncols, 4)

    def test_getitem_by_coordinate(self):
        self.assertEqual(self.grid[Coordinate(0,0)], 'a')
        self.assertEqual(self.grid[Coordinate(2,3)], 'l')

    def test_getitem_by_tuple(self):
        self.assertEqual(self.grid[(0,1)], 'b')
        self.assertEqual(self.grid[(1,2)], 'g')

    def test_setitem_by_coordinate(self):
        self.grid[Coordinate(1,1)] = 'X'
        self.assertEqual(self.grid[(1,1)], 'X')

    def test_setitem_by_tuple(self):
        self.grid[(2,0)] = 'Z'
        self.assertEqual(self.grid[(2,0)], 'Z')

    def test_in_bounds(self):
        self.assertTrue(self.grid.in_bounds(Coordinate(2,3)))
        self.assertFalse(self.grid.in_bounds(Coordinate(3,0)))
        self.assertFalse(self.grid.in_bounds(Coordinate(-1,0)))

    def test_neighbors(self):
        # Middle cell (1,1) should have all 8 neighbors
        nbrs = list(self.grid.neighbors(1,1))
        self.assertEqual(len(nbrs), 8)
        # Corner cell (0,0) should have only 3 neighbors
        nbrs_corner = list(self.grid.neighbors(0,0))
        self.assertEqual(len(nbrs_corner), 3)

    def test_items(self):
        all_items = list(self.grid.items())
        self.assertEqual(len(all_items), 3*4)
        self.assertIn((Coordinate(0,0), 'a'), all_items)
        self.assertIn((Coordinate(2,3), 'l'), all_items)

    def test_get_with_default(self):
        self.assertEqual(self.grid.get(Coordinate(0,0), default='X'), 'a')
        self.assertEqual(self.grid.get(Coordinate(10,10), default='X'), 'X')

    def test_row_values(self):
        self.assertEqual(self.grid.row_values(0), ['a','b','c','d'])
        with self.assertRaises(IndexError):
            self.grid.row_values(10)

    def test_column_values(self):
        self.assertEqual(self.grid.column_values(0), ['a','e','i'])
        with self.assertRaises(IndexError):
            self.grid.column_values(10)

    def test_find_all(self):
        coords = self.grid.find_all('a')
        self.assertEqual(coords, [Coordinate(0,0)])
        coords = self.grid.find_all('z')
        self.assertEqual(coords, [])

    def test_contains(self):
        self.assertTrue(self.grid.contains('a'))
        self.assertFalse(self.grid.contains('z'))

    def test_subgrid(self):
        sub = self.grid.subgrid(Coordinate(0,1), Coordinate(1,2))
        # should contain
        # b c
        # f g
        self.assertEqual(sub.nrows, 2)
        self.assertEqual(sub.ncols, 2)
        self.assertEqual(sub[Coordinate(0,0)], 'b')
        self.assertEqual(sub[Coordinate(1,1)], 'g')

    def test_rotate_clockwise(self):
        # original:
        # a b c d
        # e f g h
        # i j k l
        # rotate clockwise:
        # i e a
        # j f b
        # k g c
        # l h d
        rotated = self.grid.rotate_clockwise()
        self.assertEqual(rotated.nrows, 4)
        self.assertEqual(rotated.ncols, 3)
        self.assertEqual(rotated[Coordinate(0,0)], 'i')
        self.assertEqual(rotated[Coordinate(3,2)], 'd')

    def test_flip_horizontal(self):
        # flip horizontally: reverse each row
        # a b c d -> d c b a
        # e f g h -> h g f e
        # i j k l -> l k j i
        flipped = self.grid.flip_horizontal()
        self.assertEqual(flipped[Coordinate(0,0)], 'd')
        self.assertEqual(flipped[Coordinate(1,0)], 'h')

    def test_bulk_set(self):
        self.grid.bulk_set([(Coordinate(0,0),'X'), (Coordinate(2,3),'Y')])
        self.assertEqual(self.grid[Coordinate(0,0)], 'X')
        self.assertEqual(self.grid[Coordinate(2,3)], 'Y')

    def test_apply(self):
        def to_upper(coord, val):
            return val.upper()
        self.grid.apply(to_upper)
        self.assertEqual(self.grid[Coordinate(0,0)], 'A')
        self.assertEqual(self.grid[Coordinate(2,3)], 'L')

if __name__ == '__main__':
    unittest.main()
