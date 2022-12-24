from adventofcode import Solution

import re


class Day23(Solution):
    def _init(self):
        self.instructions = ['jio a, +22','inc a','tpl a','tpl a','tpl a','inc a','tpl a','inc a','tpl a','inc a','inc a','tpl a','inc a','inc a','tpl a','inc a','inc a','tpl a','inc a','inc a','tpl a','jmp +19','tpl a','tpl a','tpl a','tpl a','inc a','inc a','tpl a','inc a','tpl a','inc a','inc a','tpl a','inc a','inc a','tpl a','inc a','tpl a','tpl a','jio a, +8','inc b','jie a, +4','tpl a','inc a','jmp +2','hlf a','jmp -7']
        self.current_address = 0
        self.registers = {'a' : 0,
                          'b' : 0}

    def _reset(self):
        self.current_address = 0
        self.registers = {'a' : 0,
                          'b' : 0}

    # instruction commands
    def hlf(self, r):
        self.registers[r] /= 2
        self.current_address += 1

    def tpl(self, r):
        self.registers[r] *= 3
        self.current_address += 1

    def inc(self, r):
        self.registers[r] += 1
        self.current_address += 1

    def jmp(self, a):
        self.current_address += a

    def jie(self, r, a):
        if self.registers[r] % 2 == 0:
            self.current_address += a
        else:
            self.current_address += 1

    def jio(self, r, a):
        if self.registers[r] == 1:
            self.current_address += a
        else:
            self.current_address += 1

    def _execute_instruction(self):
        instruction = self.instructions[self.current_address]
        print(str(self.current_address) + ' : ' + instruction)

        register_set_op = re.match('^(hlf|tpl|inc) (a|b)$', instruction)
        jump_op = re.match('(jmp) ([\-\+]\d+)', instruction)
        jump_condition_op = re.match('(jie|jio) (a|b), ([\-\+]\d+)', instruction)

        if register_set_op:
            operation = getattr(self, register_set_op.group(1))
            operation(register_set_op.group(2))
        elif jump_op:
            operation = getattr(self, jump_op.group(1))
            operation(int(jump_op.group(2)))
        elif jump_condition_op:
            operation = getattr(self, jump_condition_op.group(1))
            operation(jump_condition_op.group(2), int(jump_condition_op.group(3)))
        else:
            raise Exception('invalid instruction : ' + instruction)

    def part_one(self):
        self._reset()
        while self.current_address >= 0 and self.current_address < len(self.instructions):
            self._execute_instruction()

        return self.registers

    def part_two(self):
        self._reset()
        self.registers['a'] = 1

        while self.current_address >= 0 and self.current_address < len(self.instructions):
            self._execute_instruction()

        return self.registers
