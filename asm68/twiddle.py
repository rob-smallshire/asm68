def twos_complement(n, num_bits):
    lower = -(2**(num_bits - 1))
    higher = 2**(num_bits - 1) - 1
    if not (lower <= n <= higher):
        raise ValueError("Cannot represent {} in two's complement in {} bits".format(n, num_bits))

    if n < 0:
        return n + (1 << num_bits)
    return n


def hi(b):
    return b >> 8


def lo(b):
    return b & 0xFF
