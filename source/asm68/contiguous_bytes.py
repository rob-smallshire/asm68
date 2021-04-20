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


class ContiguousBytes(Mapping):
    """A mapping from address to bytes across a continuous range of bytes.

    The mapping describes the contents of a contiguous address range, and is
    initialized by providing possibly non-contiguous but non-overlapping blocks
    of data within that range. Any addresses not covered by the provided blocks
    will contained a default value.

    """

    def __init__(self, blocks=(), *, start=None, stop=None, default=0x00):
        """
        Args:
            blocks: An iterable series of pairs with the first of each tuple being a block origin
                address, and the second being a sequence of representing the data within that block.
                The provided blocks must not overlap.

            start: The start (inclusive) address of the range of addresses in the mapping. If not
                specified the start of the block with the lowest origin address will be used.

            stop: The stop (exclusive) address of the range of addresses in the mapping. If not
                specified the address one beyond the end of the block with the highest origin will
                be used.

            default: The value of any bytes not supplied in blocks.
        """
        self._addresses = []
        self._blocks = []
        for address in sorted(blocks):
            if self._addresses:
                start_of_previous_block = self._addresses[-1]
                length_of_previous_block = len(self._blocks[-1])
                stop_of_previous_block = start_of_previous_block + length_of_previous_block
                if address < stop_of_previous_block:
                    raise ValueError(
                        f"Block with address {start_of_previous_block} with length "
                        f"{length_of_previous_block} bytes overlaps with another block with "
                        f"address {address}"
                    )
            self._addresses.append(address)
            self._blocks.append(blocks[address])

        if len(self._addresses) != 0:
            start_of_first_block = self._addresses[0]
            stop_of_last_block = self._addresses[-1] + len(self._blocks[-1])
            self._start = start if (start is not None) else start_of_first_block
            self._stop = stop if (stop is not None) else stop_of_last_block

            if self._start > start_of_first_block:
                raise ValueError(f"Start address {start} is after the beginning of the first block")

            if self._stop < stop_of_last_block:
                raise ValueError(f"Stop address {stop} is before the end of the last block")
        else:
            self._start = start or 0
            self._stop = stop or self._start

        if self._start < 0:
            raise ValueError(f"Start address {start} is not non-negative")

        if self._stop < self._start:
            raise ValueError(f"Stop address {self._stop} is before start address {self._start}")

        self._default = default
        self._keys = RangeSet(self.start, self.stop)

    @property
    def start(self):
        return self._start

    @property
    def stop(self):
        return self._stop

    def keys(self) -> RangeSet:
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