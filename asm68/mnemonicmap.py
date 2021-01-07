from frozendict import frozendict

from asm68.instructions import *
from asm68.directives import *

# TODO: Build this automatically
MNEMONIC_TO_STATEMENT = frozendict({
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
    BITMD: Bitmd,
    BEQ: Beq,
    BHS: Bhs,
    BLO: Blo,
    BNE: Bne,
    BPL: Bpl,
    BRA: Bra,
    CLRA: Clra,
    CLRB: Clrb,
    CLR: Clr,
    CMPA: Cmpa,
    CMPB: Cmpb,
    CMPD: Cmpd,
    CMPS: Cmps,
    CMPU: Cmpu,
    CMPR: Cmpr,
    CMPX: Cmpx,
    CMPY: Cmpy,
    COMA: Coma,
    COMB: Comb,
    COM: Com,
    CWAI: Cwai,
    DAA: Daa,
    DECA: Deca,
    DECB: Decb,
    DECD: Decd,
    DECE: Dece,
    DECF: Decf,
    DECW: Decw,
    DEC: Dec,
    EORA: Eora,
    EORB: Eorb,
    EXG: Exg,
    INCA: Inca,
    INCB: Incb,
    INCD: Incd,
    INCE: Ince,
    INCF: Incf,
    INCW: Incw,
    INC: Inc,
    JMP: Jmp,
    JSR: Jsr,
    LBRA: Lbra,
    LBNE: Lbne,
    LDA: Lda,
    LDB: Ldb,
    LDD: Ldd,
    LDE: Lde,
    LDF: Ldf,
    LDMD: Ldmd,
    LDQ: Ldq,
    LDS: Lds,
    LDU: Ldu,
    LDW: Ldw,
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
    STE: Ste,
    STF: Stf,
    STQ: Stq,
    STS: Sts,
    STU: Stu,
    STW: Stw,
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
    FDB: Fdb,
    CALL: Call,
})
from asm68.mnemonics import *

