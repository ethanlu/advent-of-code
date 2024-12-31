from __future__ import annotations
from adventofcode.common import Solution
from typing import List, Set


def pages_before(updates: List[int], target: int) -> Set[int]:
    before = []
    for p in updates:
        if p == target:
            break
        before.append(p)
    return set(before)


class Day05(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._rules = {}
        self._updates = []
        self._invalid_updates = []
        reading_rules = True
        for line in self._load_input_as_lines():
            if line:
                if reading_rules:
                    page, page_successor = map(lambda i: int(i), line.split('|'))
                    if page not in self._rules:
                        self._rules[page] = set([])
                    self._rules[page].update({page_successor})
                else:
                    self._updates.append(list(map(lambda i: int(i), line.split(','))))
            else:
                reading_rules = False

    def part_one(self):
        total = 0
        for update in self._updates:
            for page, required_after in self._rules.items():
                if page in update:
                    if required_after.intersection(pages_before(update, page)):
                        # at least 1 page that must be updated after was updated before the current page was updated
                        self._invalid_updates.append(update)
                        break
            else:
                # passed all rules
                middle = update[len(update) // 2]
                print(f"{update} passes page ordering rules and has middle page: {middle}")
                total += middle
        return total


    def part_two(self):
        total = 0
        for update in self._invalid_updates:
            corrected_update = update
            for page, required_after in self._rules.items():
                if page in corrected_update:
                    before = []
                    after = []
                    seen_p = False
                    for p in corrected_update:
                        if p == page:
                            before.append(p)
                            seen_p = True
                        else:
                            if p in required_after:
                                after.append(p)
                            else:
                                if seen_p:
                                    after.append(p)
                                else:
                                    before.append(p)
                    corrected_update = before + after
            middle = corrected_update[len(corrected_update) // 2]
            print(f"{corrected_update} corrected and has middle page: {middle}")
            total += middle
        return total
    