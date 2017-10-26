from frozendict import frozendict

from asm68.instructions import *
from asm68.directives import *
from asm68.mnemonics import *

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
    ORG: Org,
    FCB: Fcb,
})