from __future__ import annotations
from adventofcode.common import Solution
from functools import reduce
from itertools import chain, islice
from typing import Iterable, List, TypeVar


class BITSPacket(object):
    def __init__(self, version: str):
        self._version = int(version, 2)
        self._bit_size = 3

    @property
    def version(self) -> int:
        return self._version

    @property
    def bit_size(self) -> int:
        return self._bit_size

    def value(self) -> int:
        return -1


BP = TypeVar('BP', bound=BITSPacket)


class LiteralPacket(BITSPacket):
    def __init__(self, stream: BITSStream, version: str):
        super().__init__(version)
        self._bit_size += 3
        self._value = ''
        while True:
            literal_group = stream.read(5)
            self._value = self._value + literal_group[1:]
            self._bit_size += 5
            if literal_group[0] == '0':
                break

    def value(self) -> int:
        return int(self._value, 2)

    def show(self, tabs: str = "") -> None:
        print(f"{tabs}v{self.version}: {self.__class__.__name__} with bit size {self.bit_size} and value {self.value()}")


class OperatorPacket(BITSPacket):
    def __init__(self, stream: BITSStream, version: str):
        super().__init__(version)
        self._bit_size += 3
        self._packets = []
        self._mode = stream.read(1)
        self._bit_size += 1
        match self._mode:
            case '0':
                self._mode_length = int(stream.read(15), 2)
                self._bit_size += 15
                bits_read = 0
                while True:
                    sp = stream.parse_packet()
                    bits_read += sp.bit_size
                    self._bit_size += sp.bit_size
                    self._packets.append(sp)
                    if bits_read == self._mode_length:
                        break
                    if bits_read > self._mode_length:
                        raise Exception(f"unexpected bits read amount exceeded")
            case '1':
                self._mode_length = int(stream.read(11), 2)
                self._bit_size += 11
                for _ in range(self._mode_length):
                    sp = stream.parse_packet()
                    self._bit_size += sp.bit_size
                    self._packets.append(sp)

    @property
    def packets(self) -> List[BP]:
        return self._packets

    def show(self, tabs: str = "") -> None:
        print(f"{tabs}v{self.version}: {self.__class__.__name__} with {len(self.packets)} subpackets")
        for sp in self.packets:
            sp.show(tabs + "\t")


class SumOperatorPacket(OperatorPacket):
    def __init__(self, stream: BITSStream, version: str):
        super().__init__(stream, version)

    def value(self) -> int:
        return sum((sp.value() for sp in self.packets))


class ProductOperatorPacket(OperatorPacket):
    def __init__(self, stream: BITSStream, version: str):
        super().__init__(stream, version)

    def value(self) -> int:
        return reduce(lambda v, sp: v * sp.value(), self.packets, 1)


class MinOperatorPacket(OperatorPacket):
    def __init__(self, stream: BITSStream, version: str):
        super().__init__(stream, version)

    def value(self) -> int:
        return min((sp.value() for sp in self.packets))


class MaxOperatorPacket(OperatorPacket):
    def __init__(self, stream: BITSStream, version: str):
        super().__init__(stream, version)

    def value(self) -> int:
        return max((sp.value() for sp in self.packets))


class GreaterThanOperatorPacket(OperatorPacket):
    def __init__(self, stream: BITSStream, version: str):
        super().__init__(stream, version)

    def value(self) -> int:
        if len(self.packets) != 2:
            raise Exception(f"greater than operator packet has unexpected subpacket length : {len(self.packets)}")
        return 1 if self.packets[0].value() > self.packets[1].value() else 0


class LessThanOperatorPacket(OperatorPacket):
    def __init__(self, stream: BITSStream, version: str):
        super().__init__(stream, version)

    def value(self) -> int:
        if len(self.packets) != 2:
            raise Exception(f"less than operator packet has unexpected subpacket length : {len(self.packets)}")
        return 1 if self.packets[0].value() < self.packets[1].value() else 0


class EqualToOperatorPacket(OperatorPacket):
    def __init__(self, stream: BITSStream, version: str):
        super().__init__(stream, version)

    def value(self) -> int:
        if len(self.packets) != 2:
            raise Exception(f"equal to operator packet has unexpected subpacket length : {len(self.packets)}")
        return 1 if self.packets[0].value() == self.packets[1].value() else 0


class BITSStream(object):
    def __init__(self, stream: Iterable):
        self._stream = stream

    def read(self, n: int) -> str:
        data = ''.join(list(islice(self._stream, n)))
        if len(data) != n:
            raise Exception(f"unexpected datastream end when trying to read {n} bits")
        return data

    def parse_packet(self) -> BP:
        version = self.read(3)
        type_id = int(self.read(3), 2)
        match type_id:
            case 0:
                return SumOperatorPacket(self, version)
            case 1:
                return ProductOperatorPacket(self, version)
            case 2:
                return MinOperatorPacket(self, version)
            case 3:
                return MaxOperatorPacket(self, version)
            case 4:
                return LiteralPacket(self, version)
            case 5:
                return GreaterThanOperatorPacket(self, version)
            case 6:
                return LessThanOperatorPacket(self, version)
            case 7:
                return EqualToOperatorPacket(self, version)
            case _:
                raise Exception(f"unexpected packet type id : {type_id}")


class Day16(Solution):
    def __init__(self, year: str, day: str):
        super().__init__(year, day)
        self._bs = BITSStream(chain.from_iterable(chain((f"{int(h, 16):04b}" for h in self._load_input_as_string()))))
        self._packet = self._bs.parse_packet()

    def part_one(self):
        def add_versions(p: BP) -> int:
            match p:
                case LiteralPacket():
                    return p.version
                case _:
                    return p.version + sum((add_versions(sp) for sp in p.packets))
        self._packet.show()
        return add_versions(self._packet)

    def part_two(self):
        return self._packet.value()
