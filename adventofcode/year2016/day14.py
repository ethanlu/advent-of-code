from __future__ import annotations
from adventofcode.common import Solution
from collections import deque
from dataclasses import dataclass
from functools import reduce
from typing import Deque, Dict

import hashlib
import re


@dataclass
class OTPKey:
    index: int
    key: str
    character: str


class OTP(object):
    def __init__(self, salt: str):
        self._salt = salt
        self._hash_cache: Dict[int, str] = {}
        self._candidates: Deque[OTPKey] = deque([])
        self._confirms: Dict[int, OTPKey] = {}
        self._repeat3_regex = re.compile(r'([a-z0-9])\1{2}')
        self._repeat5_regex = re.compile(r'([a-z0-9])\1{4}')
        self._hash_stretch = False

    def _hash(self, i: int) -> str:
        if i not in self._hash_cache:
            if self._hash_stretch:
                self._hash_cache[i] = reduce(lambda acc, h: hashlib.md5(str(acc).encode('utf-8')).hexdigest(), range(0, 2016), hashlib.md5((self._salt + str(i)).encode('utf-8')).hexdigest())
            else:
                self._hash_cache[i] = hashlib.md5((self._salt + str(i)).encode('utf-8')).hexdigest()

        return self._hash_cache[i]

    def hash_stretch(self, toggle: bool) -> OTP:
        self._hash_stretch = toggle
        return self

    def generate(self, amount: int) -> OTPKey:
        keys = []

        i = 0
        while len(keys) < amount:
            # get next candidate
            try:
                candidate_key = self._candidates.popleft()
                i = candidate_key.index + 1
            except:
                # candidates queue is empty, so generate next hash until first 3-repeat is encountered
                candidate_key = None
                while candidate_key is None:
                    md5hash = self._hash(i)
                    candidate_match = self._repeat3_regex.search(md5hash)

                    if candidate_match:
                        candidate_key = OTPKey(i, md5hash, candidate_match.groups()[0])
                    i += 1

            max_j = i + 1000
            j = i
            # candidate retrieved....look for next 1000 to see if there is a 5-repeat
            for (confirm_index, confirm_key) in ((k, v) for (k, v) in self._confirms.items() if i <= k < max_j):
                j = confirm_index
                # check to see if any of the memoized confirms match
                if confirm_key.character == candidate_key.character:
                    keys.append(candidate_key)
                    print(f"({len(keys)}/{amount}) : key at {candidate_key.index} [{candidate_key.key}] with confirmation at {confirm_key.index} [{confirm_key.key}] ({confirm_key.index - candidate_key.index} away)")
                    break
            else:
                # memoized confirms do not contain any match, keep searching until reached max 1000
                while j < max_j:
                    md5hash = self._hash(j)

                    candidate_match = self._repeat3_regex.search(md5hash)
                    if candidate_match and self._candidates.count(OTPKey(j, md5hash, candidate_match.groups()[0])) == 0:
                        self._candidates.append(OTPKey(j, md5hash, candidate_match.groups()[0]))

                    confirm_match = self._repeat5_regex.search(md5hash)
                    if confirm_match:
                        if confirm_match.groups()[0] == candidate_key.character:
                            keys.append(candidate_key)
                            print(f"({len(keys)}/{amount}) : key at {candidate_key.index} [{candidate_key.key}] with confirmation at {j} [{md5hash}] ({j - candidate_key.index} away)")
                            break
                        elif j not in self._confirms:
                            # a match, but does not match candidate key character...save it for future use
                            self._confirms[j] = OTPKey(j, md5hash, confirm_match.groups()[0])
                    j += 1

        return keys[-1]


class Day14(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = self._load_input_as_string()

    def part_one(self):
        otp = OTP(self._input)
        candidate_key = otp.generate(64)

        return candidate_key.index

    def part_two(self):
        otp = OTP(self._input)
        otp.hash_stretch(True)
        candidate_key = otp.generate(64)

        return candidate_key.index
