from bisect import bisect_right
from collections.abc import Sequence, Set, Mapping
from asm68.util import typename


class RangeSet(Set, Sequence):

    def __init__(self, start, stop):
        self._r = range(start, stop)

    @property
    def start(self):
        return self._r.start

    @property
    def stop(self):
        return self._r.stop

    def __iter__(self):
        return iter(self._r)

    def __contains__(self, key):
        return key in self._r

    def __getitem__(self, index):
        return self._r[index]

    def __len__(self):
        return len(self._r)

    def __repr__(self):
        return f"{typename(self)}(start={self.start}, stop={self.stop})"


class ContinuousBytes(Mapping):

    def __init__(self, blocks, *, start=None, stop=None, default=0x00):
        # TODO: Check that blocks don't overlap
        self._addresses, self._blocks = zip(*((address, blocks[address]) for address in sorted(blocks)))
        if len(self._addresses) != 0:
            self._start = start if (start is not None) else self._addresses[0]
            self._stop = stop if (stop is not None) else self._addresses[-1] + len(self._blocks[-1])
        else:
            self._start = 0
            self._stop = 0
        self._default = default
        self._keys = RangeSet(self.start, self.stop)

    @property
    def start(self):
        return self._start

    @property
    def stop(self):
        return self._stop

    def keys(self):
        return self._keys

    def __iter__(self):
        return iter(self._keys)

    def __len__(self):
        return len(self._keys)

    def __getitem__(self, k):
        if k not in self.keys():
            raise KeyError(f"Key {k} not in {self!r}")
        index_after = bisect_right(self._addresses, k)
        if index_after != 0:
            index = index_after - 1
            address = self._addresses[index]
            block = self._blocks[index]
            if address <= k < address + len(block):
                return block[k - address]
        return self._default

    def __repr__(self):
        return f"{typename(self)}(start={self.start}, stop={self.stop})"

    def to_bytes(self):
        return bytes(self.values())