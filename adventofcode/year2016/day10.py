from collections import deque
from adventofcode.common import Solution

import re


class Bot(object):
    def __init__(self):
        self._values = deque([])

    def get_low(self):
        return self._values.popleft()

    def get_high(self):
        return self._values.pop()

    def set(self, value):
        if len(self._values) == 0:
            self._values.append(value)
        elif len(self._values) == 1:
            if self._values[0] > value:
                self._values.appendleft(value)
            else:
                self._values.append(value)
        else:
            raise Exception('You done messed up!')

    def has_two_chips(self):
        return len(self._values) == 2


class Day10(Solution):
    bot_regex = re.compile('bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)')
    value_regex = re.compile('value (\d+) goes to bot (\d+)')

    def __init__(self, year: str, day: str):
        super().__init__(year, day)

        self._num_bots = -1
        self._num_outputs = -1
        self._value_instructions = []
        self._bot_instructions = []

        for l in self._load_input_as_lines():
            r = self.bot_regex.findall(l.strip())
            if r:
                self._bot_instructions.append({'bot': int(r[0][0]), 'low_target': r[0][1], 'low_id': int(r[0][2]), 'high_target': r[0][3], 'high_id': int(r[0][4])})

                if int(r[0][0]) > self._num_bots:
                    self._num_bots = int(r[0][0])
                if r[0][1] == 'bot' and int(r[0][2]) > self._num_bots:
                    self._num_bots = int(r[0][2])
                if r[0][3] == 'bot' and int(r[0][4]) > self._num_bots:
                    self._num_bots = int(r[0][4])
                if r[0][1] == 'output' and int(r[0][2]) > self._num_outputs:
                    self._num_outputs = int(r[0][2])
                if r[0][3] == 'output' and int(r[0][4]) > self._num_outputs:
                    self._num_outputs = int(r[0][4])
            else:
                r = self.value_regex.findall(l.strip())
                self._value_instructions.append({'bot': int(r[0][1]), 'value': int(r[0][0])})

                if int(r[0][1]) > self._num_bots:
                    self._num_bots = int(r[0][1])

        self._num_bots += 1
        self._num_outputs += 1

    def _run(self, low_check, high_check):
        bots = [Bot() for i in range(self._num_bots)]
        outputs = [None for i in range(self._num_outputs)]
        flagged_bot = None

        # run through value instructions to give some of the bots some chips
        for instruction in self._value_instructions:
            bots[instruction['bot']].set(instruction['value'])

        # now continue to process the bot instructions until no more are left
        remaining_instructions = deque(self._bot_instructions)
        while len(remaining_instructions) > 0:
            instruction = remaining_instructions.popleft()

            if bots[instruction['bot']].has_two_chips():
                # bot for current instruction has two chips...so can execute
                low_value = bots[instruction['bot']].get_low()
                high_value = bots[instruction['bot']].get_high()

                if instruction['low_target'] == 'bot':
                    # giving low value to bot
                    bots[instruction['low_id']].set(low_value)
                else:
                    # giving low value to output
                    outputs[instruction['low_id']] = low_value

                if instruction['high_target'] == 'bot':
                    # giving high value to bot
                    bots[instruction['high_id']].set(high_value)
                else:
                    # giving high value to output
                    outputs[instruction['high_id']] = high_value

                if low_check == low_value and high_check == high_value:
                    flagged_bot = instruction['bot']
            else:
                # bot for current instruction does not have two chips yet...skip
                remaining_instructions.append(instruction)

        return (bots, outputs, flagged_bot)

    def part_one(self):
        # O(n^2) time complexity (n is number of instructions for bots to give values)
        # O(m) space complexity (m is  max(# of bots, # of outputs))
        bots, outputs, flagged_bot = self._run(17, 61)
        return flagged_bot

    def part_two(self):
        # O(n^2) time complexity (n is number of instructions for bots to give values)
        # O(m) space complexity (m is max(# of bots, # of outputs))
        bots, outputs, flagged_bot = self._run(17, 61)
        return outputs[0] * outputs[1] * outputs[2]
