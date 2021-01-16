from abc import abstractmethod, ABC

from asm68.mnemonics import *
from asm68.opcodes import OPCODES
from asm68.registers import A, B, D, S, U, X, Y, CC, MD, W, E, F, Q
from asm68.statement import Statement


class Instruction(Statement):

    def __init__(self, operand, comment='', label=None):
        addressing_modes = set(operand.codes)
        if OPCODES[self.mnemonic].keys().isdisjoint(addressing_modes):
            raise TypeError("Invalid {} addressing mode for {}"
                .format((type(operand).__name__).lower(), self.mnemonic))
        super().__init__(operand, comment, label)

    def assemble_operand(self, operand, opcode_key, asm):
        asm.assemble_operand(operand, opcode_key, self)


class InherentOperandAcceptable:

    def inherent_operand(self, operand, opcode_key, asm):
        return asm.assemble_inherent_operand(operand, opcode_key, self)


class InterRegisterOperandAcceptable:

    def register_operand(self, operand, opcode_key, asm):
        return asm.assemble_register_operand(operand, opcode_key, self)


class ImmediateOperandAcceptable:

    def immediate_operand(self, operand, opcode_key, asm):
        return asm.assemble_immediate_operand(operand, opcode_key, self)


class PageDirectOperandAcceptable:

    def page_direct_operand(self, operand, opcode_key, asm):
        return asm.assemble_page_direct_operand(operand, opcode_key, self)


class ExtendedDirectOperandAcceptable:

    def extended_direct_operand(self, operand, opcode_key, asm):
        return asm.assemble_extended_direct_operand(operand, opcode_key, self)


class ShortRelativeOperandAcceptable:

    def relative_operand(self, operand, opcode_key, asm):
        return asm.assemble_short_relative_operand(operand, opcode_key, self)


class LongRelativeOperandAcceptable:

    def relative_operand(self, operand, opcode_key, asm):
        return asm.assmeble_long_relative_operand(operand, opcode_key, self)


class IndexedOperandAcceptable:

    def indexed_operand(self, operand, opcode_key, asm):
        return asm.assemble_indexed_operand(operand, opcode_key, statement)


class AddressOperandAcceptable(
    PageDirectOperandAcceptable,
    IndexedOperandAcceptable,
    ExtendedDirectOperandAcceptable,
):
    pass



# TODO: Make these classes automatically

class Abx(Instruction, InherentOperandAcceptable):
    mnemonic = ABX


class Adca(
    Instruction,
    ImmediateOperandAcceptable,
    AddressOperandAcceptable,
):
    inherent_register = A
    mnemonic = ADCA


class Adcb(
    Instruction,
    ImmediateOperandAcceptable,
    AddressOperandAcceptable,
):
    inherent_register = B
    mnemonic = ADCB


class Adcd(
    Instruction,
    ImmediateOperandAcceptable,
    AddressOperandAcceptable,
):
    inherent_register = D
    mnemonic = ADCD


class Adcr(
    Instruction,
    InterRegisterOperandAcceptable,
):
    mnemonic = ADCR



class Adda(
    Instruction,
    ImmediateOperandAcceptable,
    AddressOperandAcceptable,
):
    inherent_register = A
    mnemonic = ADDA


class Addb(
    Instruction,
    ImmediateOperandAcceptable,
    AddressOperandAcceptable,
):
    inherent_register = B
    mnemonic = ADDB


class Addd(
    Instruction,
    ImmediateOperandAcceptable,
    AddressOperandAcceptable,
):
    inherent_register = D
    mnemonic = ADDD


class Adde(
    Instruction,
    ImmediateOperandAcceptable,
    AddressOperandAcceptable,
):
    inherent_register = E
    mnemonic = ADDE


class Addf(
    Instruction,
    ImmediateOperandAcceptable,
    AddressOperandAcceptable,
):
    inherent_register = F
    mnemonic = ADDF


class Addr(
    Instruction,
    InterRegisterOperandAcceptable
):
    mnemonic = ADDR


class Addw(
    Instruction,
    ImmediateOperandAcceptable,
    AddressOperandAcceptable,
):
    inherent_register = W
    mnemonic = ADDW


class Anda(Instruction):
    inherent_register = A
    mnemonic = ANDA


class Andb(Instruction):
    inherent_register = B
    mnemonic = ANDB


class Andcc(Instruction):
    inherent_register = CC
    mnemonic = ANDCC


class Asla(Instruction):
    inherent_register = A
    mnemonic = ASLA


class Aslb(Instruction):
    inherent_register = B
    mnemonic = ASLB


class Asl(Instruction):
    mnemonic = ASL


class Asra(Instruction):
    inherent_register = A
    mnemonic = ASRA


class Asrb(Instruction):
    inherent_register = B
    mnemonic = ASRB


class Asr(Instruction):
    mnemonic = ASR


class Beq(Instruction):
    mnemonic = BEQ


class Bita(Instruction):
    inherent_register = A
    mnemonic = BITA


class Bitb(Instruction):
    inherent_register = B
    mnemonic = BITB


class Bitmd(Instruction):
    inherent_register = MD
    mnemonic = BITMD


class Bhs(Instruction):
    mnemonic = BHS


class Blo(Instruction):
    mnemonic = BLO


class Bne(Instruction):
    mnemonic = BNE


class Bpl(Instruction):
    mnemonic = BPL


class Bra(Instruction):
    mnemonic = BRA


class Clra(Instruction):
    inherent_register = A
    mnemonic = CLRA


class Clrb(Instruction):
    inherent_register = B
    mnemonic = CLRB


class Clr(Instruction):
    mnemonic = CLR


class Cmpa(Instruction):
    inherent_register = A
    mnemonic = CMPA


class Cmpb(Instruction):
    inherent_register = B
    mnemonic = CMPB


class Cmpd(Instruction):
    inherent_register = D
    mnemonic = CMPD


class Cmpr(Instruction):
    mnemonic = CMPR


class Cmps(Instruction):
    inherent_register = S
    mnemonic = CMPS


class Cmpu(Instruction):
    inherent_register = U
    mnemonic = CMPU


class Cmpx(Instruction):
    inherent_register = X
    mnemonic = CMPX


class Cmpy(Instruction):
    inherent_register = Y
    mnemonic = CMPY


class Coma(Instruction):
    inherent_register = A
    mnemonic = COMA


class Comb(Instruction):
    inherent_register = B
    mnemonic = COMB


class Com(Instruction):
    mnemonic = COM


class Cwai(Instruction):
    mnemonic = CWAI


class Daa(Instruction):
    mnemonic = DAA


class Deca(Instruction):
    inherent_register = A
    mnemonic = DECA


class Decb(Instruction):
    inherent_register = B
    mnemonic = DECB


class Decd(Instruction):
    inherent_register = D
    mnemonic = DECD


class Dece(Instruction):
    inherent_register = E
    mnemonic = DECE


class Decf(Instruction):
    inherent_register = F
    mnemonic = DECF


class Decw(Instruction):
    inherent_register = W
    mnemonic = DECW


class Dec(Instruction):
    mnemonic = DEC



class Eora(Instruction):
    inherent_register = A
    mnemonic = EORA


class Eorb(Instruction):
    inherent_register = B
    mnemonic = EORB


class Exg(Instruction):
    mnemonic = EXG


class Inca(Instruction):
    inherent_register = A
    mnemonic = INCA


class Incb(Instruction):
    inherent_register = B
    mnemonic = INCB


class Incd(Instruction):
    inherent_register = D
    mnemonic = INCD


class Ince(Instruction):
    inherent_register = E
    mnemonic = INCE


class Incf(Instruction):
    inherent_register = F
    mnemonic = INCF


class Incw(Instruction):
    inherent_register = W
    mnemonic = INCW


class Inc(Instruction):
    mnemonic = INC


class Jmp(Instruction):
    mnemonic = JMP


class Jsr(Instruction):
    mnemonic = JSR


class Lbra(Instruction):
    mnemonic = LBRA


class Lbne(Instruction):
    mnemonic = LBNE


class Lda(Instruction):
    inherent_register = A
    mnemonic = LDA


class Ldb(Instruction):
    inherent_register = B
    mnemonic = LDB


class Ldd(Instruction):
    inherent_register = D
    mnemonic = LDD


class Lde(Instruction):
    inherent_register = E
    mnemonic = LDE


class Ldf(Instruction):
    inherent_register = F
    mnemonic = LDF


class Ldq(Instruction):
    inherent_register = Q
    mnemonic = LDQ


class Ldw(Instruction):
    inherent_register = W
    mnemonic = LDW


class Ldmd(Instruction):
    inherent_register = MD
    mnemonic = LDMD

class Lds(Instruction):
    inherent_register = S
    mnemonic = LDS


class Ldu(Instruction):
    inherent_register = U
    mnemonic = LDU


class Ldx(Instruction):
    inherent_register = X
    mnemonic = LDX


class Ldy(Instruction):
    inherent_register = Y
    mnemonic = LDY


class Leas(Instruction):
    inherent_register = S
    mnemonic = LEAS


class Leau(Instruction):
    inherent_register = U
    mnemonic = LEAU


class Leax(Instruction):
    inherent_register = X
    mnemonic = LEAX


class Leay(Instruction):
    inherent_register = Y
    mnemonic = LEAY


class Lsla(Instruction):
    inherent_register = A
    mnemonic = LSLA


class Lslb(Instruction):
    inherent_register = B
    mnemonic = LSLB


class Lsl(Instruction):
    mnemonic = LSL


class Lsra(Instruction):
    inherent_register = A
    mnemonic = LSRA


class Lsrb(Instruction):
    inherent_register = B
    mnemonic = LSRB


class Lsr(Instruction):
    mnemonic = LSR


class Mul(Instruction):
    mnemonic = MUL


class Nega(Instruction):
    inherent_register = A
    mnemonic = NEGA


class Negb(Instruction):
    inherent_register = B
    mnemonic = NEGB


class Neg(Instruction):
    mnemonic = NEG


class Nop(Instruction):
    mnemonic = NOP


class Ora(Instruction):
    inherent_register = A
    mnemonic = ORA


class Orb(Instruction):
    inherent_register = B
    mnemonic = ORB


class Orcc(Instruction):
    inherent_register = CC
    mnemonic = ORCC


class Pshs(Instruction):
    mnemonic = PSHS


class Pshu(Instruction):
    mnemonic = PSHU


class Puls(Instruction):
    mnemonic = PULS


class Pulu(Instruction):
    mnemonic = PULU


class Rola(Instruction):
    inherent_register = A
    mnemonic = ROLA


class Rolb(Instruction):
    inherent_register = B
    mnemonic = ROLB


class Rol(Instruction):
    mnemonic = ROL


class Rora(Instruction):
    inherent_register = A
    mnemonic = RORA


class Rorb(Instruction):
    inherent_register = B
    mnemonic = RORB


class Ror(Instruction):
    mnemonic = ROR


class Rti(Instruction):
    mnemonic = RTI


class Rts(Instruction):
    mnemonic = RTS


class Sbca(Instruction):
    inherent_register = A
    mnemonic = SBCA


class Sbcb(Instruction):
    inherent_register = B
    mnemonic = SBCB


class Sex(Instruction):
    mnemonic = SEX


class Sta(Instruction):
    inherent_register = A
    mnemonic = STA


class Stb(Instruction):
    inherent_register = B
    mnemonic = STB


class Std(Instruction):
    inherent_register = D
    mnemonic = STD


class Ste(Instruction):
    inherent_register = E
    mnemonic = STE


class Stf(Instruction):
    inherent_register = F
    mnemonic = STF


class Stq(Instruction):
    inherent_register = Q
    mnemonic = STQ


class Sts(Instruction):
    inherent_register = S
    mnemonic = STS


class Stu(Instruction):
    inherent_register = U
    mnemonic = STU


class Stw(Instruction):
    inherent_register = W
    mnemonic = STW


class Stx(Instruction):
    inherent_register = X
    mnemonic = STX


class Sty(Instruction):
    inherent_register = Y
    mnemonic = STY


class Suba(Instruction):
    inherent_register = A
    mnemonic = SUBA


class Subb(Instruction):
    inherent_register = B
    mnemonic = SUBB


class Subd(Instruction):
    inherent_register = D
    mnemonic = SUBD


class Swi(Instruction):
    mnemonic = SWI


class Swi2(Instruction):
    mnemonic = SWI2


class Swi3(Instruction):
    mnemonic = SWI3


class Sync(Instruction):
    mnemonic = SYNC


class Tfr(Instruction):
    mnemonic = TFR



class Tsta(Instruction):
    inherent_register = A
    mnemonic = TSTA


class Tstb(Instruction):
    inherent_register = B
    mnemonic = TSTB


class Tst(Instruction):
    mnemonic = TST
