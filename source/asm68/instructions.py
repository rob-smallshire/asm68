import sys

from asm68 import mnemonics
from asm68 import registers
from asm68.addrmodecodes import INT, INH, IMM, DIR, IDX, EXT, REL8, REL16
from asm68.opcodes import OPCODES
from asm68.statement import Statement
from asm68.stringutil import upper_first, uppercase_ending


class Instruction(Statement):

    def __init__(self, operand, comment='', label=None):
        addressing_modes = set(operand.codes)
        if OPCODES[self.mnemonic.key].keys().isdisjoint(addressing_modes):
            raise TypeError("Invalid {} addressing mode for {}"
                .format((type(operand).__name__).lower(), self.mnemonic))
        super().__init__(operand, comment, label)

    def assemble_operand(self, operand, opcode_key, asm, opcode_bytes):
        return asm.assemble_operand(operand, opcode_key, self, opcode_bytes)


class InherentOperandAcceptable:

    def inherent_operand(self, operand, opcode_key, asm, opcode_bytes):
        return asm.assemble_inherent_operand(operand, opcode_key, self, opcode_bytes)


class InterRegisterOperandAcceptable:

    def register_operand(self, operand, opcode_key, asm, opcode_bytes):
        return asm.assemble_register_operand(operand, opcode_key, self, opcode_bytes)


class ImmediateOperandAcceptable:

    def immediate_operand(self, operand, opcode_key, asm, opcode_bytes):
        return asm.assemble_immediate_operand(operand, opcode_key, self, opcode_bytes)


class PageDirectOperandAcceptable:

    def page_direct_operand(self, operand, opcode_key, asm, opcode_bytes):
        return asm.assemble_page_direct_operand(operand, opcode_key, self, opcode_bytes)


class ExtendedDirectOperandAcceptable:

    def extended_direct_operand(self, operand, opcode_key, asm, opcode_bytes):
        return asm.assemble_extended_direct_operand(operand, opcode_key, self, opcode_bytes)


class ShortRelativeOperandAcceptable:

    def relative_operand(self, operand, opcode_key, asm, opcode_bytes):
        return asm.assemble_short_relative_operand(operand, opcode_key, self, opcode_bytes)


class LongRelativeOperandAcceptable:

    def relative_operand(self, operand, opcode_key, asm, opcode_bytes):
        return asm.assemble_long_relative_operand(operand, opcode_key, self, opcode_bytes)


class IndexedOperandAcceptable:

    def indexed_operand(self, operand, opcode_key, asm, opcode_bytes):
        return asm.assemble_indexed_operand(operand, opcode_key, self, opcode_bytes)


this_module = sys.modules[__name__]
print(this_module)

for opcode, modes in OPCODES.items():
    name = upper_first(opcode)
    print(name)
    inherent_name = uppercase_ending(opcode)
    bases = tuple(
        filter(
            None,
            (
                Instruction,
                (INH in modes) and InherentOperandAcceptable,
                (INT in modes) and InterRegisterOperandAcceptable,
                (IMM in modes) and ImmediateOperandAcceptable,
                (DIR in modes) and PageDirectOperandAcceptable,
                (IDX in modes) and IndexedOperandAcceptable,
                (EXT in modes) and ExtendedDirectOperandAcceptable,
                (REL8 in modes) and ShortRelativeOperandAcceptable,
                (REL16 in modes) and LongRelativeOperandAcceptable
            )
        )
    )
    members = {
        k: v for k, v in {
            "__module__": this_module,
            "mnemonic": getattr(mnemonics, opcode.upper()),
            "inherent_register": inherent_name and getattr(registers, inherent_name),
        }.items() if v
    }
    cls = type(
        name,
        bases,
        members
    )
    globals()[name] = cls

