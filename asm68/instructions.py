from asm68.mnemonics import *
from asm68.opcodes import OPCODES
from asm68.registers import A, B, D, S, U, X, Y, CC
from asm68.statement import Statement


class Instruction(Statement):

    def __init__(self, operand, comment='', label=None):
        if OPCODES[self.mnemonic].keys().isdisjoint(operand.codes):
            raise TypeError("Invalid {} addressing mode for {}"
                            .format((type(operand).__name__).lower(), self.mnemonic))
        super().__init__(operand, comment, label)

class Abx(Instruction):
    mnemonic = ABX


class Adca(Instruction):
    inherent_register = A
    mnemonic = ADCA


class Adcb(Instruction):
    inherent_register = B
    mnemonic = ADCB


class Adda(Instruction):
    inherent_register = A
    mnemonic = ADDA


class Addb(Instruction):
    inherent_register = B
    mnemonic = ADDB


class Addd(Instruction):
    inherent_register = D
    mnemonic = ADDD


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


class Bita(Instruction):
    inherent_register = A
    mnemonic = BITA


class Bitb(Instruction):
    inherent_register = B
    mnemonic = BITB


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


class Sts(Instruction):
    inherent_register = S
    mnemonic = STS


class Stu(Instruction):
    inherent_register = U
    mnemonic = STU


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



