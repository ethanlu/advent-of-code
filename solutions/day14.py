import re

input = ['Vixen can fly 8 km/s for 8 seconds, but then must rest for 53 seconds.','Blitzen can fly 13 km/s for 4 seconds, but then must rest for 49 seconds.','Rudolph can fly 20 km/s for 7 seconds, but then must rest for 132 seconds.','Cupid can fly 12 km/s for 4 seconds, but then must rest for 43 seconds.','Donner can fly 9 km/s for 5 seconds, but then must rest for 38 seconds.','Dasher can fly 10 km/s for 4 seconds, but then must rest for 37 seconds.','Comet can fly 3 km/s for 37 seconds, but then must rest for 76 seconds.','Prancer can fly 9 km/s for 12 seconds, but then must rest for 97 seconds.','Dancer can fly 37 km/s for 1 seconds, but then must rest for 36 seconds.']

class Day14(object):
    def __init__(self, reindeers):
        self.reindeers = {}

        for i in reindeers:
            r = re.match('^(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds\.$', i)

            if r is None:
                raise Exception('invalid input : ' + i)

            self.reindeers[r.group(1)] = {'speed': int(r.group(2)),
                                          'speed_duration': int(r.group(3)),
                                          'rest_duration': int(r.group(4))}

    def _get_longest_distance(self, reindeer_states):
        longest_distance = 0
        for r in reindeer_states:
            if longest_distance == 0 or longest_distance < reindeer_states[r]['distance_traveled']:
                longest_distance = reindeer_states[r]['distance_traveled']

        return longest_distance

    def _get_highest_points(self, reindeer_states):
        highest_points = 0
        for r in reindeer_states:
            if highest_points == 0 or highest_points < reindeer_states[r]['points']:
                highest_points = reindeer_states[r]['points']

        return highest_points

    def _race(self, time):
        reindeer_states = {r: {'distance_traveled': 0, 'points': 0, 'resting': False, 'duration_left': self.reindeers[r]['speed_duration']} for r in self.reindeers}

        for t in xrange(time):
            for r in self.reindeers:
                if reindeer_states[r]['resting']:
                    # reindeer is resting
                    if reindeer_states[r]['duration_left'] > 0:
                        reindeer_states[r]['duration_left'] -= 1

                    if reindeer_states[r]['duration_left'] == 0:
                        reindeer_states[r]['resting'] = False
                        reindeer_states[r]['duration_left'] = self.reindeers[r]['speed_duration']
                else:
                    # reindeer is moving
                    if reindeer_states[r]['duration_left'] > 0:
                        reindeer_states[r]['duration_left'] -= 1
                        reindeer_states[r]['distance_traveled'] += self.reindeers[r]['speed']

                    if reindeer_states[r]['duration_left'] == 0:
                        reindeer_states[r]['resting'] = True
                        reindeer_states[r]['duration_left'] = self.reindeers[r]['rest_duration']

            longest_distance = self._get_longest_distance(reindeer_states)
            for r in self.reindeers:
                if longest_distance == reindeer_states[r]['distance_traveled']:
                    reindeer_states[r]['points'] += 1

        return reindeer_states

    def part_one(self):
        return self._get_longest_distance(self._race(2503))

    def part_two(self):
        return self._get_highest_points(self._race(2503))
