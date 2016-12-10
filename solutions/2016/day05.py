import hashlib


class Day05(object):
    def __init__(self, input_file):
        with open(input_file) as f:
            self._input = f.read().strip()

    def part_one(self):
        # O(n) time complexity (n is search space of md5 hash with 5 leading zeroes)
        # O(c) space complexity
        password = ['?', '?', '?', '?', '?', '?', '?', '?']
        found = 0
        i = 0
        while found < 8:
            attempt = '{id}{i}'.format(id=self._input, i=i)
            s = hashlib.md5(attempt.encode()).hexdigest()

            if s[:5] == '00000':
                print('{s} found at index {i}'.format(s=s, i=i))
                password[found] = s[5]
                found += 1

            i += 1

        return ''.join(password)

    def part_two(self):
        # O(n) time complexity (n is search space of md5 hash with 5 leading zeroes and 6th character between 0 and 7)
        # O(c) space complexity
        password = ['?', '?', '?', '?', '?', '?', '?', '?']
        found = 0
        i = 0
        while found < 8:
            attempt = '{id}{i}'.format(id=self._input, i=i)
            s = hashlib.md5(attempt.encode()).hexdigest()

            if s[:5] == '00000' and s[5] in ('0', '1', '2', '3', '4', '5', '6', '7') and password[int(s[5])] == '?':
                print('{s} found at index {i}'.format(s=s, i=i))
                password[int(s[5])] = s[6]
                found += 1

            i += 1

        return ''.join(password)

if __name__ == '__main__':
    p = Day05('../../input/2016/day05.txt')

    print('-----part one-----')
    print(p.part_one())

    print('-----part two-----')
    print(p.part_two())
