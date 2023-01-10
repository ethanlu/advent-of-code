from adventofcode import Solution

import re

class Day14(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)

        self._reindeers = {}

        for l in self._load_input_as_lines():
            r = re.match('^(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds\.$', l)

            if r is None:
                raise Exception('invalid input : ' + l)

            self._reindeers[r.group(1)] = {'speed': int(r.group(2)),
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
        reindeer_states = {r: {'distance_traveled': 0, 'points': 0, 'resting': False, 'duration_left': self._reindeers[r]['speed_duration']} for r in self._reindeers}

        for t in range(time):
            for r in self._reindeers:
                if reindeer_states[r]['resting']:
                    # reindeer is resting
                    if reindeer_states[r]['duration_left'] > 0:
                        reindeer_states[r]['duration_left'] -= 1

                    if reindeer_states[r]['duration_left'] == 0:
                        reindeer_states[r]['resting'] = False
                        reindeer_states[r]['duration_left'] = self._reindeers[r]['speed_duration']
                else:
                    # reindeer is moving
                    if reindeer_states[r]['duration_left'] > 0:
                        reindeer_states[r]['duration_left'] -= 1
                        reindeer_states[r]['distance_traveled'] += self._reindeers[r]['speed']

                    if reindeer_states[r]['duration_left'] == 0:
                        reindeer_states[r]['resting'] = True
                        reindeer_states[r]['duration_left'] = self._reindeers[r]['rest_duration']

            longest_distance = self._get_longest_distance(reindeer_states)
            for r in self._reindeers:
                if longest_distance == reindeer_states[r]['distance_traveled']:
                    reindeer_states[r]['points'] += 1

        return reindeer_states

    def part_one(self):
        return self._get_longest_distance(self._race(2503))

    def part_two(self):
        return self._get_highest_points(self._race(2503))
