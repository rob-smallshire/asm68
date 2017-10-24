# content of conftest.py
from itertools import zip_longest


def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, bytes) and isinstance(right, bytes) and op == "==":
        return ['Comparing bytes collections:',
                ' left: {}'.format(' '.join(format(b, '02X') for b in left)),
                'right: {}'.format(' '.join(format(b, '02X') for b in right)),
                '       {}'.format(' '.join('  ' if l==r else '^^' for l, r in zip_longest(left, right)))
                ]
