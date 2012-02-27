#!/usr/bin/env python
# solver.py

import sys # required for argv and exit

class Board:
  GRID_SIZE = 9

  def __init__(self, file):
    self.grid = []
    self.fixed_cells = []
    self.load_file(file)
    self.validate()

  def load_file(self, file):
    for row_num, line in enumerate(file):
      row = self.load_row(line, row_num)
      if row: self.grid.append(row)
    return self.grid

  def load_row(self, line, row_num):
    row = []
    for char_num, char in enumerate(list(line.strip())):
      point = (row_num, char_num/2)
      cell = self.load_cell(char, point)
      if cell: row.append(cell)
    return row

  def load_cell(self, char, point):
    if char == ' ': return None
    cell = Cell(char, self, point)
    if cell.fixed:
      self.fixed_cells.append(cell)
    return cell

  def print_grid(self):
    for row in self.grid:
      for cell in row:
        print cell,
      print

  def solve(self):
    for cell in self.fixed_cells:
      self.breed(cell)

  def breed(self, cell):
    for sibling in cell.get_siblings():
      if sibling.abandon(cell) and sibling.is_solved():
        self.breed(sibling)

  def validate(self):
    if len(self.grid) != self.GRID_SIZE:
      print "puzzle grid must contain %s rows" % self.GRID_SIZE
      sys.exit()

    for row in self.grid:
      if len(row) != self.GRID_SIZE:
        print "each row must contain %s cells" % self.GRID_SIZE
        sys.exit()

class Cell:
  ALLOWED_VALUES = range(1, Board.GRID_SIZE+1)
  BLANK_CHAR = '_'

  def __init__(self, char, board, point):
    self.board = board
    self.point = point
    self.siblings = None
    if char == self.BLANK_CHAR:
      self.fixed = False
      self.values = self.ALLOWED_VALUES[:]
    else:
      self.fixed = True
      try:
        value = int(char)
        if value in self.ALLOWED_VALUES:
          self.values = [value]
        else: raise ValueError()
      except ValueError:
        print "invalid cell value: %s" % char
        sys.exit()

  def __repr__(self):
    if self.is_solved():
      return str(self.values[0])
    else:
      return self.BLANK_CHAR

  def abandon(self, cell):
    value = cell.values[0]
    if value in self.values:
      assert not self.is_solved()
      self.values.remove(value)
      return True
    else:
      return False

  def get_siblings(self):
    if self.siblings: return self.siblings
    my_row, my_col = self.point
    siblings = []
    for row_num, row in enumerate(self.board.grid):
      if row_num == my_row: siblings += row                 # collect siblings in my row
      for col_num, cell in enumerate(row):
        if col_num == my_col: siblings.append(cell)         # collect siblings in my column
        if row_num/3 == my_row/3 and col_num/3 == my_col/3: # collect siblings in my local 3x3 grid
          siblings.append(cell)
    siblings = list(set(siblings)) # remove duplicates
    siblings.remove(self)          # remove self
    self.siblings = siblings
    return siblings

  def is_solved(self):
    return self.fixed | len(self.values) == 1


if len(sys.argv) != 2:
  print "usage: python solver.py <file>"
  sys.exit()

puzzle_file = open(sys.argv[1], 'r')

board = Board(puzzle_file)
board.print_grid()
board.solve()
print; board.print_grid()
