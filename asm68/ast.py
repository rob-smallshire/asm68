from frozendict import frozendict

from asm68.mnemonics import *
from asm68.opcodes import OPCODES
from asm68.registers import A, B, D, S, U, X, Y, CC


class Statement:

    mnemonic = None

    def __init__(self, operand, comment='', label=None):
        if OPCODES[self.mnemonic].keys().isdisjoint(operand.codes):
            raise TypeError("Invalid {} addressing mode for {}"
                            .format((type(operand).__name__).lower(), self.mnemonic))
        self._operand = operand
        self._comment = comment
        self._label = label

    def __repr__(self):
        return "{}(operand={!r}, label={!r})".format(self.__class__.__name__, self._operand, self._label)

    def __eq__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return self._is_equal(rhs)

    def __hash__(self):
        return hash((self.mnemonic, self.operand, self.comment, self.label))

    def _is_equal(self, rhs):
        return (self.mnemonic == rhs.mnemonic) and (self._operand == rhs._operand) and (self._comment == rhs._comment) and (self._label == rhs._label)

    @property
    def operand(self):
        return self._operand

    @property
    def comment(self):
        return self._comment

    @property
    def label(self):
        return self._label


class Abx(Statement):
    mnemonic = ABX


class Adca(Statement):
    inherent_register = A
    mnemonic = ADCA


class Adcb(Statement):
    inherent_register = B
    mnemonic = ADCB


class Adda(Statement):
    inherent_register = A
    mnemonic = ADDA


class Addb(Statement):
    inherent_register = B
    mnemonic = ADDB


class Addd(Statement):
    inherent_register = D
    mnemonic = ADDD


class Anda(Statement):
    inherent_register = A
    mnemonic = ANDA


class Andb(Statement):
    inherent_register = B
    mnemonic = ANDB


class Andcc(Statement):
    inherent_register = CC
    mnemonic = ANDCC


class Asla(Statement):
    inherent_register = A
    mnemonic = ASLA


class Aslb(Statement):
    inherent_register = B
    mnemonic = ASLB


class Asl(Statement):
    mnemonic = ASL


class Asra(Statement):
    inherent_register = A
    mnemonic = ASRA


class Asrb(Statement):
    inherent_register = B
    mnemonic = ASRB


class Asr(Statement):
    mnemonic = ASR


class Bita(Statement):
    inherent_register = A
    mnemonic = BITA


class Bitb(Statement):
    inherent_register = B
    mnemonic = BITB


class Bhs(Statement):
    mnemonic = BHS


class Blo(Statement):
    mnemonic = BLO


class Clra(Statement):
    inherent_register = A
    mnemonic = CLRA


class Clrb(Statement):
    inherent_register = B
    mnemonic = CLRB


class Clr(Statement):
    mnemonic = CLR


class Cmpa(Statement):
    inherent_register = A
    mnemonic = CMPA


class Cmpb(Statement):
    inherent_register = B
    mnemonic = CMPB


class Cmpd(Statement):
    inherent_register = D
    mnemonic = CMPD


class Cmps(Statement):
    inherent_register = S
    mnemonic = CMPS


class Cmpu(Statement):
    inherent_register = U
    mnemonic = CMPU


class Cmpx(Statement):
    inherent_register = X
    mnemonic = CMPX


class Cmpy(Statement):
    inherent_register = Y
    mnemonic = CMPY


class Coma(Statement):
    inherent_register = A
    mnemonic = COMA


class Comb(Statement):
    inherent_register = B
    mnemonic = COMB


class Com(Statement):
    mnemonic = COM


class Cwai(Statement):
    mnemonic = CWAI


class Daa(Statement):
    mnemonic = DAA


class Deca(Statement):
    inherent_register = A
    mnemonic = DECA


class Decb(Statement):
    inherent_register = B
    mnemonic = DECB


class Dec(Statement):
    mnemonic = DEC


class Eora(Statement):
    inherent_register = A
    mnemonic = EORA


class Eorb(Statement):
    inherent_register = B
    mnemonic = EORB


class Exg(Statement):
    mnemonic = EXG


class Inca(Statement):
    inherent_register = A
    mnemonic = INCA


class Incb(Statement):
    inherent_register = B
    mnemonic = INCB


class Inc(Statement):
    mnemonic = INC


class Jmp(Statement):
    mnemonic = JMP


class Jsr(Statement):
    mnemonic = JSR


class Lda(Statement):
    inherent_register = A
    mnemonic = LDA


class Ldb(Statement):
    inherent_register = B
    mnemonic = LDB


class Ldd(Statement):
    inherent_register = D
    mnemonic = LDD


class Lds(Statement):
    inherent_register = S
    mnemonic = LDS


class Ldu(Statement):
    inherent_register = U
    mnemonic = LDU


class Ldx(Statement):
    inherent_register = X
    mnemonic = LDX


class Ldy(Statement):
    inherent_register = Y
    mnemonic = LDY


class Leas(Statement):
    inherent_register = S
    mnemonic = LEAS


class Leau(Statement):
    inherent_register = U
    mnemonic = LEAU


class Leax(Statement):
    inherent_register = X
    mnemonic = LEAX


class Leay(Statement):
    inherent_register = Y
    mnemonic = LEAY


class Lsla(Statement):
    inherent_register = A
    mnemonic = LSLA


class Lslb(Statement):
    inherent_register = B
    mnemonic = LSLB


class Lsl(Statement):
    mnemonic = LSL


class Lsra(Statement):
    inherent_register = A
    mnemonic = LSRA


class Lsrb(Statement):
    inherent_register = B
    mnemonic = LSRB


class Lsr(Statement):
    mnemonic = LSR


class Mul(Statement):
    mnemonic = MUL


class Nega(Statement):
    inherent_register = A
    mnemonic = NEGA


class Negb(Statement):
    inherent_register = B
    mnemonic = NEGB


class Neg(Statement):
    mnemonic = NEG


class Nop(Statement):
    mnemonic = NOP


class Ora(Statement):
    inherent_register = A
    mnemonic = ORA


class Orb(Statement):
    inherent_register = B
    mnemonic = ORB


class Orcc(Statement):
    inherent_register = CC
    mnemonic = ORCC


class Pshs(Statement):
    mnemonic = PSHS


class Pshu(Statement):
    mnemonic = PSHU


class Puls(Statement):
    mnemonic = PULS


class Pulu(Statement):
    mnemonic = PULU


class Rola(Statement):
    inherent_register = A
    mnemonic = ROLA


class Rolb(Statement):
    inherent_register = B
    mnemonic = ROLB


class Rol(Statement):
    mnemonic = ROL


class Rora(Statement):
    inherent_register = A
    mnemonic = RORA


class Rorb(Statement):
    inherent_register = B
    mnemonic = RORB


class Ror(Statement):
    mnemonic = ROR


class Rti(Statement):
    mnemonic = RTI


class Rts(Statement):
    mnemonic = RTS


class Sbca(Statement):
    inherent_register = A
    mnemonic = SBCA


class Sbcb(Statement):
    inherent_register = B
    mnemonic = SBCB


class Sex(Statement):
    mnemonic = SEX


class Sta(Statement):
    inherent_register = A
    mnemonic = STA


class Stb(Statement):
    inherent_register = B
    mnemonic = STB


class Std(Statement):
    inherent_register = D
    mnemonic = STD


class Sts(Statement):
    inherent_register = S
    mnemonic = STS


class Stu(Statement):
    inherent_register = U
    mnemonic = STU


class Stx(Statement):
    inherent_register = X
    mnemonic = STX


class Sty(Statement):
    inherent_register = Y
    mnemonic = STY


class Suba(Statement):
    inherent_register = A
    mnemonic = SUBA


class Subb(Statement):
    inherent_register = B
    mnemonic = SUBB


class Subd(Statement):
    inherent_register = D
    mnemonic = SUBD


class Swi(Statement):
    mnemonic = SWI


class Swi2(Statement):
    mnemonic = SWI2


class Swi3(Statement):
    mnemonic = SWI3


class Sync(Statement):
    mnemonic = SYNC


class Tfr(Statement):
    mnemonic = TFR


class Tsta(Statement):
    inherent_register = A
    mnemonic = TSTA


class Tstb(Statement):
    inherent_register = B
    mnemonic = TSTB


class Tst(Statement):
    mnemonic = TST


MNEMONIC_TO_AST = frozendict({
    ABX: Abx,
    ADCA: Adca,
    ADCB: Adcb,
    ADDA: Adda,
    ADDB: Addb,
    ADDD: Addd,
    ANDA: Anda,
    ANDB: Andb,
    ANDCC: Andcc,
    ASLA: Asla,
    ASLB: Aslb,
    ASL: Asl,
    ASRA: Asra,
    ASRB: Asrb,
    ASR: Asr,
    BITA: Bita,
    BITB: Bitb,
    BHS: Bhs,
    BLO: Blo,
    CLRA: Clra,
    CLRB: Clrb,
    CLR: Clr,
    CMPA: Cmpa,
    CMPB: Cmpb,
    CMPD: Cmpd,
    CMPS: Cmps,
    CMPU: Cmpu,
    CMPX: Cmpx,
    CMPY: Cmpy,
    COMA: Coma,
    COMB: Comb,
    COM: Com,
    CWAI: Cwai,
    DAA: Daa,
    DECA: Deca,
    DECB: Decb,
    DEC: Dec,
    EORA: Eora,
    EORB: Eorb,
    EXG: Exg,
    INCA: Inca,
    INCB: Incb,
    INC: Inc,
    JMP: Jmp,
    JSR: Jsr,
    LDA: Lda,
    LDB: Ldb,
    LDD: Ldd,
    LDS: Lds,
    LDU: Ldu,
    LDX: Ldx,
    LDY: Ldy,
    LEAS: Leas,
    LEAU: Leau,
    LEAX: Leax,
    LEAY: Leay,
    LSLA: Lsla,
    LSLB: Lslb,
    LSL: Lsl,
    LSRA: Lsra,
    LSRB: Lsrb,
    LSR: Lsr,
    MUL: Mul,
    NEGA: Nega,
    NEGB: Negb,
    NEG: Neg,
    NOP: Nop,
    ORA: Ora,
    ORB: Orb,
    ORCC: Orcc,
    PSHS: Pshs,
    PSHU: Pshu,
    PULS: Puls,
    PULU: Pulu,
    ROLA: Rola,
    ROLB: Rolb,
    ROL: Rol,
    RORA: Rora,
    RORB: Rorb,
    ROR: Ror,
    RTI: Rti,
    RTS: Rts,
    SBCA: Sbca,
    SBCB: Sbcb,
    SEX: Sex,
    STA: Sta,
    STB: Stb,
    STD: Std,
    STS: Sts,
    STU: Stu,
    STX: Stx,
    STY: Sty,
    SUBA: Suba,
    SUBB: Subb,
    SUBD: Subd,
    SWI: Swi,
    SWI2: Swi2,
    SWI3: Swi3,
    SYNC: Sync,
    TFR: Tfr,
    TSTA: Tsta,
    TSTB: Tstb,
    TST: Tst,
})


