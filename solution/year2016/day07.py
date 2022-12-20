from solution import Solution

import re


class Day07(Solution):
    abba_regex = re.compile('(?P<A>[a-z])(?P<B>[a-z])(?P=B)(?P=A)')
    in_bracket_strings_regex = re.compile('\[([a-z]+)\]')
    out_bracket_strings_regex = re.compile('\[[a-z]+\]')

    def _init(self):
        self._input = [l.strip() for l in self._load_input_as_lines()]

    def _is_abba(self, s):
        return sum([1 for a, b in self.abba_regex.findall(s) if a != b]) > 0

    def _is_bab(self, s):
        return sum([1 for a, b in self.bab_regex.findall(s) if a != b]) > 0

    def part_one(self):
        # O(n) time complexity (n is number of lines in input)
        # O(n) space complexity (n is number of lines in input)
        valid_count = 0
        for input in self._input:
            num_abbas = sum([1 for s in self.in_bracket_strings_regex.findall(input) if self._is_abba(s)])
            if num_abbas == 0:
                # no abbas found for strings within brackets...now find abbas for everything
                valid_count += 1 if sum([1 for s in self.out_bracket_strings_regex.split(input) if self._is_abba(s)]) > 0 else 0

        return valid_count

    def part_two(self):
        # O(nm) time complexity (n is number of messages in input, m is length of lines)
        # O(n) space complexity (n is number of lines in input)
        valid_count = 0

        for input in self._input:
            in_brackets = self.in_bracket_strings_regex.findall(input)
            out_brackets = self.out_bracket_strings_regex.split(input)

            try:
                for os in out_brackets:
                    for i in range(len(os) - 2):
                        if os[i] != os[i + 1] and os[i] == os[i + 2]:
                            for s in in_brackets:
                                if s.find('{b}{a}{b}'.format(a=os[i], b=os[i + 1])) != -1:
                                    valid_count += 1
                                    raise
            except:
                pass

        return valid_count
