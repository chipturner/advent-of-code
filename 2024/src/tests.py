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

class TestBaseMethods(unittest.TestCase):
    def test_grid_methods(self):
        g = Grid.from_list_of_strings(["abc","def"])
        self.assertTrue(g.contains('a'))
        self.assertFalse(g.contains('z'))
        self.assertEqual(g.find_all('a'), [Coordinate(0,0)])
        coords_values = [(Coordinate(0,1),'X'), (Coordinate(1,2),'Y')]
        g.bulk_set(coords_values)
        self.assertEqual(g[Coordinate(0,1)], 'X')
        self.assertEqual(g[Coordinate(1,2)], 'Y')
        def to_upper(coord, val): return val.upper()
        g.apply(to_upper)
        self.assertEqual(g[Coordinate(0,1)], 'X')
        self.assertEqual(g[Coordinate(1,2)], 'Y')

    def test_sparse_methods(self):
        s = SparseGrid(default='.')
        s[Coordinate(0,0)] = 'a'
        s[Coordinate(10,10)] = 'b'
        self.assertTrue(s.contains('a'))
        self.assertFalse(s.contains('z'))
        self.assertEqual(s.find_all('b'), [Coordinate(10,10)])
        s.bulk_set([(Coordinate(5,5),'X')])
        self.assertEqual(s.get(Coordinate(5,5)), 'X')
        def lower(coord, val): return val.lower()
        s.apply(lower)
        self.assertEqual(s[Coordinate(0,0)], 'a')
        self.assertEqual(s.get(Coordinate(1,1)), '.')

class TestConversion(unittest.TestCase):
    def test_to_sparse(self):
        g = Grid.from_list_of_strings(["abc", "def"])
        s = to_sparse(g)
        self.assertEqual(s.get(Coordinate(0,0)), 'a')
        self.assertEqual(s.get(Coordinate(1,2)), 'f')
        self.assertEqual(s.get(Coordinate(10,10)), None)

    def test_to_dense(self):
        s = SparseGrid(default='X')
        s[Coordinate(0,0)] = 'a'
        s[Coordinate(2,3)] = 'b'
        dense = to_dense(s, Coordinate(0,0), Coordinate(2,3))
        self.assertEqual(dense[Coordinate(0,0)], 'a')
        self.assertEqual(dense[Coordinate(2,3)], 'b')
        self.assertEqual(dense[Coordinate(1,1)], 'X')

if __name__ == '__main__':
    unittest.main()
