import pytest

from asm68.asmdsl import AsmDsl, statements
from asm68.assembler import assemble


def check_object_code(machine_code, instruction, operand=None):
    __tracebackhide__ = True
    asm = AsmDsl()
    if operand is None:
        asm(instruction)
    else:
        asm(instruction, operand)
    code = assemble(statements(asm))
    actual_code = code[0]
    expected_code = bytes.fromhex(machine_code)
    if actual_code != expected_code:
        pytest.fail("{instruction} {operand!r} assembled to {actual} not {expected}".format(
            instruction=instruction,
            operand=operand,
            actual=' '.join(format(b, '02X') for b in actual_code),
            expected=' '.join(format(b, '02X') for b in expected_code),
        ))