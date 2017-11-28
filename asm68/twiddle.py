def twos_complement(n, num_bits):
    if num_bits < 1:
        raise ValueError("Two's complement cannot be represented in less than 1 bit")
    lower = -(1 << (num_bits - 1))
    higher = (1 << (num_bits - 1)) - 1
    if not (lower <= n <= higher):
        raise ValueError("Cannot represent {} in two's complement in {} bits".format(n, num_bits))
    return n % (1 << num_bits)


def hi(b):
    return b >> 8


def lo(b):
    return b & 0xFF
