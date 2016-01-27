import hashlib

class Day04(object):
    def __init__(self, key):
        self.key = key

    def mine(self, l):
        pattern = '0'*l
        i = 0
        while True:
            i += 1
            print 'mining...' + str(i)
            if hashlib.md5(self.key + str(i)).hexdigest()[0:l] == pattern:
                break
        return i

    def part_one(self):
        return self.mine(5)

    def part_two(self):
        return self.mine(6)
