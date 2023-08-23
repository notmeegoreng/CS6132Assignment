import io
import ipaddress
from typing import Generic, TypeVar

IP_ADDRESS = ipaddress.IPv4Address | ipaddress.IPv6Address
IP_INTERFACE = ipaddress.IPv4Interface | ipaddress.IPv6Interface


T = TypeVar('T')


class RoutingTable(Generic[T]):
    def __init__(self, interfaces: dict[T, IP_INTERFACE] | None = None):
        self.interfaces: dict[T, IP_INTERFACE] = interfaces or {}
        self.default_interface: IP_INTERFACE | None = None

    def route(self, dest: IP_ADDRESS) -> tuple[T, IP_INTERFACE] | tuple[None, None]:
        for ident, interface in self.interfaces.items():
            if dest in interface.network:
                return ident, interface
        return None, None

    def store(self, file: io.TextIOBase):
        with file as f:
            for ident, interface in self.interfaces.items():
                f.write(f'{ident}|{interface.with_prefixlen}\n')

    @classmethod
    def load(cls, file: io.TextIOBase):
        inst = cls()
        with file as f:
            for line in f.readlines():
                ident, interface = line.rstrip().split('|')
                inst.interfaces[ident] = ipaddress.ip_interface(interface)
        return inst
