from adventofcode.common import Solution


class Day18(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)

        self._grid_dimension = 100
        self._corners_always_on = False
        self._state = []

        self._initial_setup = "".join([l.strip() for l in self._load_input_as_lines()])

    def _force_always_on_check(self):
        if self._corners_always_on:
            self._state[0][0] = True
            self._state[self._grid_dimension - 1][0] = True
            self._state[0][self._grid_dimension - 1] = True
            self._state[self._grid_dimension - 1][self._grid_dimension - 1] = True

    def _reset(self):
        self._state = [[False for x in range(self._grid_dimension)] for y in range(self._grid_dimension)]

        for x, state in enumerate(self._initial_setup):
            self._state[(x // self._grid_dimension)][(x % self._grid_dimension)] = True if state == '#' else False

        self._force_always_on_check()

    def _get_cell_state(self, x, y):
        if x < 0 or x >= self._grid_dimension or y < 0 or y >= self._grid_dimension:
            return False
        else:
            return self._state[x][y]

    def _num_on(self):
        on_states = 0
        for x in range(self._grid_dimension):
            for y in range(self._grid_dimension):
                if self._state[x][y]:
                    on_states += 1

        return on_states

    def _step(self):
        next_state = [[False for x in range(self._grid_dimension)] for y in range(self._grid_dimension)]
        for x in range(self._grid_dimension):
            for y in range(self._grid_dimension):
                surrounding_states = [self._get_cell_state(x - 1, y - 1), self._get_cell_state(x, y - 1), self._get_cell_state(x + 1, y - 1),
                                      self._get_cell_state(x - 1, y),                                     self._get_cell_state(x + 1, y),
                                      self._get_cell_state(x - 1, y + 1), self._get_cell_state(x, y + 1), self._get_cell_state(x + 1, y + 1)]

                num_on = len([c for c in surrounding_states if c])

                if self._state[x][y]:
                    # current cell is on, stays on if either 2 or 3 surrounding neighbors are on, turns off otherwise
                    next_state[x][y] = True if num_on in (2, 3) else False
                else:
                    # current cell is off, turns on if exaclty 3 surrounding neighbors are on, stays off otherwise
                    next_state[x][y] = True if num_on in (3,) else False

        self._state = next_state
        self._force_always_on_check()

    def part_one(self):
        num_steps = 100
        self._reset()
        for i in range(num_steps):
            self._step()

        return self._num_on()

    def part_two(self):
        num_steps = 100
        self._corners_always_on = True
        self._reset()
        for i in range(num_steps):
            self._step()

        return self._num_on()
