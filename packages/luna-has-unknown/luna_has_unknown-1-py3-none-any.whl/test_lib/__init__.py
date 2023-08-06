import pymem


class SnakeMemory(pymem.Pymem):
    def get_pointer(self, static: int, offsets: list):
        _hex = self.read_int(self.base_address + static)
        for offset in offsets:
            _hex = self.read_int(_hex + offset)
        return _hex
