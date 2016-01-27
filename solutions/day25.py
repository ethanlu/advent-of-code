import re

input = 'To continue, please consult the code grid in the manual.  Enter the code at row 2981, column 3075.'

class Day25(object):
    def __init__(self, input):
        self.input = input
        r = re.match('To continue, please consult the code grid in the manual\.  Enter the code at row (\d+), column (\d+).', self.input)

        if r is None:
            raise Exception('Invalid input : ' + self.input)

        self.row = int(r.group(1))
        self.column = int(r.group(2))

    def _get_code_recursive(self, row, column):
        # NOTE : reaches max recursion depth for row, column values over 25,25
        if row == 1 and column == 1:
            return 20151125
        else:
            if column > 1:
                # based on position of this code, its previous code is one down and one left
                return ((self._get_code(row + 1, column - 1) * 252533) % 33554393)
            else:
                # based on position of this code, its previous code is at the previous diagonal position at upper right
                return ((self._get_code(1, row - 1) * 252533) % 33554393)

    def _get_code(self, target_row, target_column):
        code = 20151125
        row = 1
        column = 1

        while row != target_row or column != target_column:
            print 'code at ' + str(row) + ', ' + str(column) + ' is ' + str(code)

            if row == 1:
                # based on position of this code, the next code is the next diagonal values at the starting from lower left
                row = column + 1
                column = 1
            else:
                # based on position of this code, the next code is on the same diagonal values one up and one right of current
                row -= 1
                column += 1

            code = ((code * 252533) % 33554393)

        return code

    def part_one(self):
        return self._get_code(self.row, self.column)

    def part_two(self):
        pass
