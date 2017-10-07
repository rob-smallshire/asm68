from frozendict import frozendict

from asm68.mnemonics import *
from asm68.opcodes import OPCODES, ADDRESSING_MODE_CODES


class Statement:

    mnemonic = None

    def __init__(self, operand):
        addr_mode_code = ADDRESSING_MODE_CODES[type(operand)]
        if not addr_mode_code in OPCODES[self.mnemonic]:
            raise TypeError("Invalid {} addressing mode for {}"
                            .format((type(operand).__name__).lower(), self.mnemonic))
        self._operand = operand

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self._operand)

    def __eq__(self, rhs):
        if not isinstance(rhs, self.__class__):
            return NotImplemented
        return self._is_equal(rhs)

    def _is_equal(self, rhs):
        return self._operand == rhs._operand

    @property
    def operand(self):
        return self._operand


class Abx(Statement):
    mnemonic = ABX


class Adca(Statement):
    mnemonic = ADCA


class Adcb(Statement):
    mnemonic = ADCB


class Adda(Statement):
    mnemonic = ADDA


class Addb(Statement):
    mnemonic = ADDB


class Addd(Statement):
    mnemonic = ADDD


class Anda(Statement):
    mnemonic = ANDA


class Andb(Statement):
    mnemonic = ANDB


class Andcc(Statement):
    mnemonic = ANDCC


class Asla(Statement):
    mnemonic = ASLA


class Aslb(Statement):
    mnemonic = ASLB


class Asl(Statement):
    mnemonic = ASL


class Asra(Statement):
    mnemonic = ASRA


class Asrb(Statement):
    mnemonic = ASRB


class Asr(Statement):
    mnemonic = ASR


class Bita(Statement):
    mnemonic = BITA


class Bitb(Statement):
    mnemonic = BITB


class Clra(Statement):
    mnemonic = CLRA


class Clrb(Statement):
    mnemonic = CLRB


class Clr(Statement):
    mnemonic = CLR


class Cmpa(Statement):
    mnemonic = CMPA


class Cmpb(Statement):
    mnemonic = CMPB


class Cmpd(Statement):
    mnemonic = CMPD


class Cmps(Statement):
    mnemonic = CMPS


class Cmpu(Statement):
    mnemonic = CMPU


class Cmpx(Statement):
    mnemonic = CMPX


class Cmpy(Statement):
    mnemonic = CMPY


class Coma(Statement):
    mnemonic = COMA


class Comb(Statement):
    mnemonic = COMB


class Com(Statement):
    mnemonic = COM


class Cwai(Statement):
    mnemonic = CWAI


class Daa(Statement):
    mnemonic = DAA


class Deca(Statement):
    mnemonic = DECA


class Decb(Statement):
    mnemonic = DECB


class Dec(Statement):
    mnemonic = DEC


class Eora(Statement):
    mnemonic = EORA


class Eorb(Statement):
    mnemonic = EORB


class Exg(Statement):
    mnemonic = EXG


class Inca(Statement):
    mnemonic = INCA


class Incb(Statement):
    mnemonic = INCB


class Inc(Statement):
    mnemonic = INC


class Jmp(Statement):
    mnemonic = JMP


class Jsr(Statement):
    mnemonic = JSR


class Lda(Statement):
    mnemonic = LDA


class Ldb(Statement):
    mnemonic = LDB


class Ldd(Statement):
    mnemonic = LDD


class Lds(Statement):
    mnemonic = LDS


class Ldu(Statement):
    mnemonic = LDU


class Ldx(Statement):
    mnemonic = LDX


class Ldy(Statement):
    mnemonic = LDY


class Leas(Statement):
    mnemonic = LEAS


class Leau(Statement):
    mnemonic = LEAU


class Leax(Statement):
    mnemonic = LEAX


class Leay(Statement):
    mnemonic = LEAY


class Lsla(Statement):
    mnemonic = LSLA


class Lslb(Statement):
    mnemonic = LSLB


class Lsl(Statement):
    mnemonic = LSL


class Lsra(Statement):
    mnemonic = LSRA


class Lsrb(Statement):
    mnemonic = LSRB


class Lsr(Statement):
    mnemonic = LSR


class Mul(Statement):
    mnemonic = MUL


class Nega(Statement):
    mnemonic = NEGA


class Negb(Statement):
    mnemonic = NEGB


class Neg(Statement):
    mnemonic = NEG


class Nop(Statement):
    mnemonic = NOP


class Ora(Statement):
    mnemonic = ORA


class Orb(Statement):
    mnemonic = ORB


class Orcc(Statement):
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
    mnemonic = ROLA


class Rolb(Statement):
    mnemonic = ROLB


class Rol(Statement):
    mnemonic = ROL


class Rora(Statement):
    mnemonic = RORA


class Rorb(Statement):
    mnemonic = RORB


class Ror(Statement):
    mnemonic = ROR


class Rti(Statement):
    mnemonic = RTI


class Rts(Statement):
    mnemonic = RTS


class Sbca(Statement):
    mnemonic = SBCA


class Sbcb(Statement):
    mnemonic = SBCB


class Sex(Statement):
    mnemonic = SEX


class Sta(Statement):
    mnemonic = STA


class Stb(Statement):
    mnemonic = STB


class Std(Statement):
    mnemonic = STD


class Sts(Statement):
    mnemonic = STS


class Stu(Statement):
    mnemonic = STU


class Stx(Statement):
    mnemonic = STX


class Sty(Statement):
    mnemonic = STY


class Suba(Statement):
    mnemonic = SUBA


class Subb(Statement):
    mnemonic = SUBB


class Subd(Statement):
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
    mnemonic = TSTA


class Tstb(Statement):
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


