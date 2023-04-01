from __future__ import annotations
from adventofcode.common import Solution
from adventofcode.year2019.day09 import IntCodeCPUComplete
from collections import deque
from functools import reduce
from typing import Deque, List, Optional


class NetworkException(Exception):
    pass


class NetworkPacket(object):
    def __init__(self, address: int, x: int, y: int):
        self._address = address
        self._x = x
        self._y = y

    @property
    def address(self) -> int:
        return self._address

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y


class NetworkComputer(object):
    def __init__(self, address: int, program: List[int], switch: NetworkSwitch):
        self._address = address
        self._cpu = IntCodeCPUComplete(program)
        self._switch = switch
        self._incoming: Deque[NetworkPacket] = deque([])
        self._output = []

        self._cpu.add_input(self._address)

    @property
    def address(self) -> int:
        return self._address

    @property
    def has_incoming(self) -> bool:
        return len(self._incoming) > 0

    @property
    def need_input(self) -> bool:
        return self._cpu.need_input

    def receive(self, message: NetworkPacket):
        self._incoming.append(message)

    def run(self) -> None:
        if self._cpu.need_input:
            if len(self._incoming) > 0:
                message = self._incoming.popleft()
                self._cpu.add_input(message.x)
                self._cpu.add_input(message.y)
            else:
                self._cpu.add_input(-1)

        self._cpu.run()

        if self._cpu.has_output:
            self._output.append(self._cpu.get_output())

            if len(self._output) == 3:
                self._switch.send(self.address, NetworkPacket(*self._output))
                self._output = []


class NetworkSwitch(object):
    def __init__(self, program: List[int], use_nat: bool):
        self._program = program
        self._computers: List[NetworkComputer] = []
        self._size = 0
        self._use_nat = use_nat
        self._nat_packet = None

    @property
    def nat_packet(self) -> Optional[NetworkPacket]:
        return self._nat_packet

    def add_computer(self):
        self._computers.append(NetworkComputer(self._size, self._program, self))
        self._size += 1

    def send(self, source: int, message: NetworkPacket) -> None:
        if message.address == 255:
            self._nat_packet = message
            if not self._use_nat:
                print(f"first message sent to NAT with y={message.y}")
                raise NetworkException()
        else:
            print(f"network computer {source} sending x={message.x} and y={message.y} to network computer {message.address}")
            self._computers[message.address].receive(message)

    def run(self) -> None:
        try:
            last_nat_packet = None
            while True:
                for cpu in self._computers:
                    cpu.run()

                if self._use_nat and self._nat_packet is not None and reduce(lambda acc, c: acc and not c.has_incoming and c.need_input, self._computers, True):
                    print(f"nat detected network is idle...sending x={self._nat_packet.x} and y={self._nat_packet.y} to network computer 0")
                    self._computers[0].receive(self._nat_packet)
                    if last_nat_packet is None or last_nat_packet.y != self._nat_packet.y:
                        last_nat_packet = self._nat_packet
                    else:
                        raise NetworkException()
        except NetworkException as e:
            pass


class Day23(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._input = [int(i) for i in self._load_input_as_string().split(',')]

    def part_one(self):
        ns = NetworkSwitch(self._input, False)
        for _ in range(50):
            ns.add_computer()
        ns.run()

        return ns.nat_packet.y

    def part_two(self):
        ns = NetworkSwitch(self._input, True)
        for _ in range(50):
            ns.add_computer()
        ns.run()

        return ns.nat_packet.y
