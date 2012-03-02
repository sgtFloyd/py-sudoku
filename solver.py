#!/usr/bin/env python
# solver.py

import sys # required for argv and exit

class Board:
  """ Sudoku board representation and methods to work with it.
    Attributes:
      grid - the main data structure, contains rows of Cells
      fixed_cells - the Cells with hardcoded values
  """
  GRID_SIZE = 9

  def __init__(self, file):
    self.grid = []
    self.fixed_cells = []
    self.load_file(file)
    self.validate()

  def load_file(self, file):
    """ parse a file into the board grid structure """
    for row_num, line in enumerate(file):
      row = self.load_row(line, row_num)
      if row: self.grid.append(row)
    return self.grid

  def load_row(self, line, row_num):
    """ parse a line of text into one row of the board """
    row = []
    for char_num, char in enumerate(list(line.strip())):
      point = (row_num, char_num/2)
      cell = self.load_cell(char, point)
      if cell: row.append(cell)
    return row

  def load_cell(self, char, point):
    """ create a cell object from a character of text """
    if char == ' ': return None
    cell = Cell(char, self, point)
    if cell.is_solved():
      self.fixed_cells.append(cell)
    return cell

  def print_grid(self):
    """ print the current state of the board """
    for row in self.grid:
      for cell in row:
        print cell,
      print

  def print_grid_values(self):
    """ show remaining possible values of each cell on the board """
    av = Cell.ALLOWED_VALUES
    ranges = [av[0:3], av[3:6], av[6:9]]
    for row in self.grid:
      for values in ranges:
        for cell in row:
          for val in values:
            if val in cell.values:
              print val,
            else:
              print Cell.BLANK_CHAR,
          print ' ',
        print
      print

  def solve(self):
    """ attempt to solve this board """
    for cell in self.fixed_cells:
      self.breed(cell)
    # TODO: "only cell in cousins which could be..."
    return self.is_solved()

  def breed(self, cell):
    """ recursively propogate this cell's value to all its
        neighbors. if any of the neighbors become solved
        because of this propogation, propogate *that* cell's
        value to *its* neighbors, and so on """
    for sibling in cell.get_siblings():
      if sibling.abandon(cell) and sibling.is_solved():
        self.breed(sibling)

  def is_solved(self):
    """ return True if this board is completely solved """
    for row in self.grid:
      for cell in row:
        if not cell.is_solved():
          return False
    return True

  def validate(self):
    """ validate the dimensions of this board """
    if len(self.grid) != self.GRID_SIZE:
      print "puzzle grid must contain %s rows" % self.GRID_SIZE
      sys.exit()
    for row in self.grid:
      if len(row) != self.GRID_SIZE:
        print "each row must contain %s cells" % self.GRID_SIZE
        sys.exit()

class Cell:
  """ Represents one cell in a Sudoku board
    Attributes:
      values - possible values for this cell
      board - the game board this cell belongs to
      point - the cartesian coordinates of this cell on the board
      siblings - neighboring cells whose values must be unique from this cell
  """
  ALLOWED_VALUES = range(1, Board.GRID_SIZE+1)
  BLANK_CHAR = '_'

  def __init__(self, char, board, point):
    """ set the initial values of this cell """
    self.board = board
    self.point = point
    self.siblings = None
    if char == self.BLANK_CHAR:
      self.values = self.ALLOWED_VALUES[:]
    else:
      try:
        value = int(char)
        if value in self.ALLOWED_VALUES:
          self.values = [value]
        else: raise ValueError()
      except ValueError:
        print "invalid cell value: %s" % char
        sys.exit()

  def __repr__(self):
    """ override the string representation of this cell """
    if self.is_solved():
      return str(self.values[0])
    else:
      return self.BLANK_CHAR

  def abandon(self, cell):
    """ given a solved cell, remove its value
        from this cell's possible values """
    assert cell.is_solved()
    value = cell.values[0]
    if value in self.values:
      assert not self.is_solved()
      self.values.remove(value)
      return True
    else:
      return False

  def get_siblings(self):
    """ gather all of this cell's 'sibling' cells. siblings
        are found in this cell's row, column, or 3x3 grid """
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

  def get_cousins(self):
    """ gather all of this cell's 'cousin' cells. cousins
        are found as the siblings of this cell's local 3x3 grid """
    return None

  def is_solved(self):
    """ return True if there is only one possible value remaining """
    return len(self.values) == 1


if len(sys.argv) != 2:
  print "usage: python solver.py <file>"
  sys.exit()

puzzle_file = open(sys.argv[1], 'r')

board = Board(puzzle_file)
board.print_grid()
solved = board.solve()
print; board.print_grid()
if not solved:
  print; board.print_grid_values()
