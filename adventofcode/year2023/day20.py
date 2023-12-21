from __future__ import annotations
from abc import abstractmethod
from adventofcode.common import Solution
from collections import deque
from functools import reduce
from math import lcm
from typing import Dict, List, Optional, Tuple, Union


class Module(object):
    def __init__(self, name: str):
        self._name = name
        self._sources: Dict[str, bool] = {}
        self._destinations: List[str] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def sources(self) -> Dict[str]:
        return self._sources

    @property
    def destinations(self) -> List[str]:
        return self._destinations

    def register_destination(self, destination: str) -> None:
        self._destinations.append(destination)

    def register_source(self, source: str) -> None:
        self._sources[source] = False

    @abstractmethod
    def relay(self, pulse: bool, source: str) -> Optional[bool]:
        raise Exception(f"Not implemented")

    @abstractmethod
    def reset(self) -> None:
        raise Exception(f"Not implemented")


class BroadcastModule(Module):
    def __init__(self, name: str):
        super().__init__(name)

    def relay(self, pulse: bool, source: str) -> Optional[bool]:
        return pulse

    def reset(self) -> None:
        pass


class FlipFlopModule(Module):
    def __init__(self, name: str):
        super().__init__(name)
        self._state = False

    def relay(self, pulse: bool, source: str) -> Optional[bool]:
        if not pulse:
            self._state = not self._state
            return self._state
        return None

    def reset(self) -> None:
        self._state = False


class ConjunctionModule(Module):
    def __init__(self, name: str):
        super().__init__(name)

    def relay(self, pulse: bool, source: str) -> Optional[bool]:
        self._sources[source] = pulse
        return not reduce(lambda x, y: x and y, self._sources.values(), True)

    def reset(self) -> None:
        self._sources = {k: False for k in self._sources.keys()}


class OutputModule(Module):
    def __init__(self, name: str):
        super().__init__(name)
        self._output = None

    @property
    def output(self) -> Optional[bool]:
        return self._output

    def relay(self, pulse: bool, source: str) -> Optional[bool]:
        self._output = pulse
        return None

    def reset(self) -> None:
        self._output = None


class Day20(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._modules: Dict[str, Union[BroadcastModule, FlipFlopModule, ConjunctionModule, OutputModule]] = {
            'output': OutputModule('output'),
            'rx': OutputModule('rx')
        }
        registers = []
        for l in self._load_input_as_lines():
            module_name, module_destinations = l.split(' -> ')
            match module_name[0], module_name[1:]:
                case 'b', 'roadcaster':
                    self._modules['broadcaster'] = BroadcastModule('broadcaster')
                    registers.append(('broadcaster', module_destinations.split(', ')))
                case '%', name:
                    self._modules[name] = FlipFlopModule(name)
                    registers.append((name, module_destinations.split(', ')))
                case '&', name:
                    self._modules[name] = ConjunctionModule(name)
                    registers.append((name, module_destinations.split(', ')))
                case _:
                    raise Exception(f"Unexpected module type : {module_name}")
        for source, destinations in registers:
            for destination in destinations:
                self._modules[source].register_destination(destination)
                self._modules[destination].register_source(source)

    def part_one(self):
        total_low, total_high = 0, 0
        for _ in range(1000):
            low = 0
            high = 0
            remaining = deque([(False, 'button', 'broadcaster')])
            while len(remaining) > 0:
                pulse, sender, receiver = remaining.pop()
                # print(f"{sender} -{'high' if pulse else 'low'}-> {receiver}")
                if pulse:
                    high += 1
                else:
                    low += 1
                relayed_pulse = self._modules[receiver].relay(pulse, sender)
                if relayed_pulse is not None:
                    for destination in self._modules[receiver].destinations:
                        remaining.appendleft((relayed_pulse, receiver, destination))
            total_low += low
            total_high += high
        print(f"{total_low} low, {total_high} high")
        return total_low * total_high

    def part_two(self):
        cm = self._modules[list(self._modules['rx'].sources.keys())[0]]
        # rx module is assumed to always have a conjunction module as a single input
        if len(self._modules['rx'].sources) != 1 or not issubclass(type(cm), ConjunctionModule):
            raise Exception(f"rx module does have have a single conjunction module as its input!")

        for m in self._modules.values():
            m.reset()

        # rx's input module is a conjunction module, so all of this conjunction module's inputs must all be high in order for rx to get a low pulse
        # for each of the conjunction module's inputs, find how many presses it takes for each to send a high pulse to calculate the lcm of them all
        cm_input_presses = {k: 0 for k in cm.sources.keys()}
        modules_to_sniff = set(cm_input_presses.keys())
        press = 0
        while len(modules_to_sniff) > 0:
            press += 1
            remaining = deque([(False, 'button', 'broadcaster')])
            while len(remaining) > 0:
                pulse, sender, receiver = remaining.pop()
                relayed_pulse = self._modules[receiver].relay(pulse, sender)
                if relayed_pulse is not None:
                    for destination in self._modules[receiver].destinations:
                        remaining.appendleft((relayed_pulse, receiver, destination))
                        if relayed_pulse and destination == cm.name and receiver in modules_to_sniff:
                            cm_input_presses[receiver] = press
                            modules_to_sniff.remove(receiver)
                            print(f"conjunction module input {receiver} received a high pulse during press {press}")
        return lcm(*cm_input_presses.values())
