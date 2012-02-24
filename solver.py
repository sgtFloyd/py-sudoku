import sys # required for argv and exit

class Board:
  GRID_SIZE = 9

  def load_file(self, file):
    self.grid = []
    for line in file:
      row = self.load_row(line)
      if row: self.grid.append(row)
    return self.grid

  def load_row(self, line):
    row = []
    for char in list(line.strip()):
      cell = self.load_cell(char)
      if cell: row.append(cell)
    return row

  def load_cell(self, char):
    if char == ' ': return None
    return Cell(char)

  def print_grid(self):
    for row in self.grid:
      print ' '.join(row)

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

  def __init__(self, char):
    if char == '_':
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

if len(sys.argv) != 2:  # the program name and one argument
  print "usage: python solver.py <file>"
  sys.exit()

puzzle_file = open(sys.argv[1], 'r')

board = Board()
board.load_file(puzzle_file)
board.validate()
