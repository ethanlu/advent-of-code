from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.common.grid import Point2D
from adventofcode.common.range import Box2D, Interval
from collections import deque
from typing import Tuple


def trajectory(velocity: Point2D, target: Box2D) -> Tuple[bool, int, int, Point2D, Point2D]:
    position = Point2D(0, 0)
    current_velocity = velocity
    steps = 0
    maxy = 0
    while True:
        steps += 1
        position = position + current_velocity
        maxy = maxy if position.y < maxy else position.y
        if current_velocity.x > 0:
            current_velocity = current_velocity + Point2D(-1, -1)
        elif current_velocity.x < 0:
            current_velocity = current_velocity + Point2D(1, -1)
        else:
            current_velocity = current_velocity + Point2D(0, -1)
        if target.contains(position):
            # position landed in target, so return results
            return True, steps, maxy, position, current_velocity
        if position.x > target.bottom_right.x:
            # position went past the target's right most x position, so will never hit target with initial velocity
            return False, steps, maxy, position, current_velocity
        if position.y < target.bottom_right.y:
            # position is below the target's bottom most y position, so will never hit target with initial velocity
            return False, steps, maxy, position, current_velocity


class Day17(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        x_interval, y_interval = (Interval(*(int(n) for n in s.split('..'))) for s in self._load_input_as_string()[15:].split(', y='))
        self._target = Box2D(Point2D(x_interval.left, y_interval.right), Point2D(x_interval.right, y_interval.left))

    def part_one(self):
        best = 0
        attempted = set()
        remaining = deque([Point2D(0, 0)])
        while len(remaining) > 0:
            velocity = remaining.popleft()
            if velocity in attempted:
                continue
            attempted.add(velocity)
            hit, steps, maxy, final_position, final_velocity = trajectory(velocity, self._target)
            if hit:
                # target was hit, update best maxy if needed and attempt new starting velocities that can reach higher
                if best < maxy:
                    best = maxy
                    print(f"velocity {velocity} hit target at {final_position} after {steps} steps with a new best height of {maxy}")
                remaining.append(velocity + Point2D(0, 1))
                remaining.append(velocity + Point2D(1, 1))
            else:
                # undershot and this was not an adjustment, so try with more x velocity
                if final_position.x < self._target.top_left.x:
                    # undershot and it was an adjustment...but it got closer...so continue adjusting
                    remaining.append(velocity + Point2D(1, 0))
                # landed in range of x position, but overshot the y position....only try a faster/slower y velocity if landed within the width of the y range of the target
                if final_position.x < self._target.bottom_right.x and abs(final_position.y - self._target.bottom_right.y) < 3 * self._target.height:
                    remaining.append(velocity + Point2D(0, 1))
        return best

    def part_two(self):
        velocities = set()
        attempted = set()
        remaining = deque([Point2D(0, 0)])
        while len(remaining) > 0:
            velocity = remaining.popleft()
            if velocity in attempted:
                continue
            attempted.add(velocity)
            hit, steps, maxy, final_position, final_velocity = trajectory(velocity, self._target)
            if hit:
                # target was hit, update best maxy if needed and attempt new starting velocities that can reach higher
                velocities.add(velocity)
                remaining.append(velocity + Point2D(0, 1))
                remaining.append(velocity + Point2D(0, -1))
                remaining.append(velocity + Point2D(1, 1))
            else:
                # undershot and this was not an adjustment, so try with more x velocity
                if final_position.x < self._target.top_left.x:
                    # undershot and it was an adjustment...but it got closer...so continue adjusting
                    remaining.append(velocity + Point2D(1, 0))
                # landed in range of x position, but overshot the y position....only try a faster/slower y velocity if landed within the width of the y range of the target
                if final_position.x < self._target.bottom_right.x and abs(final_position.y - self._target.bottom_right.y) < 5 * self._target.height:
                    remaining.append(velocity + Point2D(0, 1))
                    remaining.append(velocity + Point2D(0, -1))
        return len(velocities)
