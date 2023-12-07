from __future__ import annotations
from adventofcode.common import Solution
from collections import Counter
from functools import total_ordering
from typing import List


@total_ordering
class CamelCardHand(object):
    CARDS = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')

    def __init__(self, hand: List[str], bet: int):
        self._hand = hand
        self._bet = bet
        self._hand_counter = Counter()
        for c in self._hand:
            self._hand_counter[c] += 1

    @property
    def hand(self) -> List[str]:
        return self._hand

    @property
    def bet(self) -> int:
        return self._bet

    @property
    def value(self) -> int:
        digits = [self._hand_type()]
        for c in self._hand:
            digits.append(self.CARDS.index(c))
        return sum((pow(len(self.CARDS), i) * digit for i, digit in enumerate(reversed(digits))))

    def __str__(self):
        return ''.join(self._hand)

    def __eq__(self, other):
        return self.hand == other.hand if issubclass(type(other), CamelCardHand) else False

    def __ne__(self, other):
        return self.hand != other.hand if issubclass(type(other), CamelCardHand) else False

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def _hand_type(self) -> int:
        match [p[1] for p in self._hand_counter.most_common(5)]:
            case [5]:   # 5 of a kind
                return 7
            case [4, 1]:    # 4 of a kind
                return 6
            case [3, 2]:    # full house
                return 5
            case [3, 1, 1]: # 3 of a kind
                return 4
            case [2, 2, 1]: # 2 pairs
                return 3
            case [2, 1, 1, 1]:  # pair
                return 2
            case [1, 1, 1, 1, 1]:   # high card
                return 1
            case _:
                raise Exception(f"Unexpected card hand : {self.hand}")


@total_ordering
class CamelCardHandWithJoker(CamelCardHand):
    CARDS = ('J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A')

    def __init__(self, hand: List[str], bet: int):
        super().__init__(hand, bet)

    def _hand_type(self) -> int:
        match ([p[1] for p in self._hand_counter.most_common(5)], self._hand_counter['J']):
            case ([5], _) | ([4, 1], 1) | ([4, 1], 4) | ([3, 2], 2) | ([3, 2], 3):  # 5 of a kind
                return 7
            case ([4, 1], 0) | ([3, 1, 1], 1) | ([3, 1, 1], 3) | ([2, 2, 1], 2):    # 4 of a kind
                return 6
            case ([3, 2], 0) | ([2, 2, 1], 1):  # full house
                return 5
            case ([3, 1, 1], 0) | ([2, 1, 1, 1], 1) | ([2, 1, 1, 1], 2):    # 3 of a kind
                return 4
            case ([2, 2, 1], 0):    # 2 pairs
                return 3
            case ([2, 1, 1, 1], 0) | ([1, 1, 1, 1, 1], 1):  # pair
                return 2
            case ([1, 1, 1, 1, 1], 0):  # high card
                return 1
            case _:
                raise Exception(f"Unexpected card hand : {self.hand}")


class Day07(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._inputs = []
        for l in self._load_input_as_lines():
            t = l.split( ' ')
            self._inputs.append((list(t[0]), int(t[1])))

    def part_one(self):
        total = 0
        hands = []
        for h, b in self._inputs:
            hands.append(CamelCardHand(h, b))
        for i, hand in enumerate(sorted(hands)):
            print(f"{i + 1}: hand {hand} ({hand.value}) bets {hand.bet}")
            total += (i + 1) * hand.bet
        return total

    def part_two(self):
        total = 0
        hands = []
        for h, b in self._inputs:
            hands.append(CamelCardHandWithJoker(h, b))
        for i, hand in enumerate(sorted(hands)):
            print(f"{i + 1}: hand {hand} ({hand.value}) bets {hand.bet}")
            total += (i + 1) * hand.bet
        return total
