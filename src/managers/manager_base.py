from abc import ABC, abstractmethod
from typing import List
import struct

from collections import namedtuple


class Panel(namedtuple('Panel', ('id', 'center_x', 'center_y', 'orientation'))):
    pack_string = '!llld'

    def to_bytes(self):
        return struct.pack(Panel.pack_string, self.id, self.center_x, self.center_y, self.orientation)

    @classmethod
    def from_bytes(cls, bts):
        return Panel(*struct.unpack(Panel.pack_string, bts))

    @classmethod
    def list_from_bytes(cls, bts):
        return [Panel(*pr) for pr in struct.iter_unpack(Panel.pack_string, bts)]


class ManagerBase(ABC):
    """
    Todo: change layouts to remove the factor of 150
    """
    @abstractmethod
    def get_num_panels(self) -> int:
        pass

    @abstractmethod
    def get_layout(self) -> List[Panel]:
        pass

    @abstractmethod
    def put_colors(self, colors):
        pass
