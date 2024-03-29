from asm68.addrmodes import *

OPCODES_6809 = {
    "abX":   { INH: '3A',                                                                     },
    "adcA":  {              IMM: '89',   DIR: '99',   IDX: 'A9',   EXT: 'B9',                 },
    "adcB":  {              IMM: 'C9',   DIR: 'D9',   IDX: 'E9',   EXT: 'F9',                 },
    "addA":  {              IMM: '8B',   DIR: '9B',   IDX: 'AB',   EXT: 'BB',                 },
    "addB":  {              IMM: 'CB',   DIR: 'DB',   IDX: 'EB',   EXT: 'FB',                 },
    "addD":  {              IMM: 'C3',   DIR: 'D3',   IDX: 'E3',   EXT: 'F3',                 },
    "andA":  {              IMM: '84',   DIR: '94',   IDX: 'A4',   EXT: 'B4',                 },
    "andB":  {              IMM: 'C4',   DIR: 'D4',   IDX: 'E4',   EXT: 'F4',                 },
    "andCC": {              IMM: '1C',                                                        },
    "aslA":  { INH: '48',                                                                     },
    "aslB":  { INH: '58',                                                                     },
    "asl":   {                           DIR: '08',   IDX: '68',   EXT: '78',                 },
    "asrA":  { INH: '47',                                                                     },
    "asrB":  { INH: '57',                                                                     },
    "asr":   {                           DIR: '07',   IDX: '67',   EXT: '77',                 },
    "bcc":   {                                                                   REL8: '24'   },
    "bcs":   {                                                                   REL8: '25'   },
    "beq":   {                                                                   REL8: '27'   },
    "bitA":  {              IMM: '85',   DIR: '95',   IDX: 'A5',   EXT: 'B5',                 },
    "bitB":  {              IMM: 'C5',   DIR: 'D5',   IDX: 'E5',   EXT: 'F5',                 },
    "bhs":   {                                                                   REL8: '24'   },
    "blo":   {                                                                   REL8: '25'   },
    "bne":   {                                                                   REL8: '26'   },
    "bpl":   {                                                                   REL8: '2A'   },
    "bra":   {                                                                   REL8: '20'   },
    "clrA":  { INH: '4F',                                                                     },
    "clrB":  { INH: '5F',                                                                     },
    "clr":   {                           DIR: '0F',   IDX: '6F',   EXT: '7F',                 },
    "cmpA":  {              IMM: '81',   DIR: '91',   IDX: 'A1',   EXT: 'B1',                 },
    "cmpB":  {              IMM: 'C1',   DIR: 'D1',   IDX: 'E1',   EXT: 'F1',                 },
    "cmpD":  {              IMM: '1083', DIR: '1093', IDX: '10A3', EXT: '10B3',               },
    "cmpS":  {              IMM: '118C', DIR: '119C', IDX: '11AC', EXT: '11BC',               },
    "cmpU":  {              IMM: '1183', DIR: '1193', IDX: '11A3', EXT: '11B3',               },
    "cmpX":  {              IMM: '8C',   DIR: '9C',   IDX: 'AC',   EXT: 'BC',                 },
    "cmpY":  {              IMM: '108C', DIR: '109C', IDX: '10AC', EXT: '10BC',               },
    "comA":  { INH: '43',                                                                     },
    "comB":  { INH: '53',                                                                     },
    "com":   {                           DIR: '03',   IDX: '63',   EXT: '73',                 },
    "cwai":  {              IMM: '3C',                                                        },
    "daa":   { INH: '19',                                                                     },
    "decA":  { INH: '4A',                                                                     },
    "decB":  { INH: '5A',                                                                     },
    "dec":   {                           DIR: '0A',   IDX: '6A',   EXT: '7A',                 },
    "eorA":  {              IMM: '88',   DIR: '98',   IDX: 'A8',   EXT: 'B8',                 },
    "eorB":  {              IMM: 'C8',   DIR: 'D8',   IDX: 'E8',   EXT: 'F8',                 },
    "exg":   {              INT: '1E',                                                        },
    "incA":  { INH: '4C',                                                                     },
    "incB":  { INH: '5C',                                                                     },
    "inc":   {                           DIR: '0C',   IDX: '6C',   EXT: '7C',                 },
    "jmp":   {                           DIR: '0E',   IDX: '6E',   EXT: '7E',                 },
    "jsr":   {                           DIR: '9D',   IDX: 'AD',   EXT: 'BD',                 },
    "lbra":  {                                                                  REL16: '16'   },
    "lbne":  {                                                                  REL16: '1026' },
    "ldA":   {              IMM: '86',   DIR: '96',   IDX: 'A6',   EXT: 'B6',                 },
    "ldB":   {              IMM: 'C6',   DIR: 'D6',   IDX: 'E6',   EXT: 'F6',                 },
    "ldD":   {              IMM: 'CC',   DIR: 'DC',   IDX: 'EC',   EXT: 'FC',                 },
    "ldS":   {              IMM: '10CE', DIR: '10DE', IDX: '10EE', EXT: '10FE',               },
    "ldU":   {              IMM: 'CE',   DIR: 'DE',   IDX: 'EE',   EXT: 'FE',                 },
    "ldX":   {              IMM: '8E',   DIR: '9E',   IDX: 'AE',   EXT: 'BE',                 },
    "ldY":   {              IMM: '108E', DIR: '109E', IDX: '10AE', EXT: '10BE',               },
    "leaS":  {                                        IDX: '32',                              },
    "leaU":  {                                        IDX: '33',                              },
    "leaX":  {                                        IDX: '30',                              },
    "leaY":  {                                        IDX: '31',                              },
    "lslA":  { INH: '48',                                                                     },
    "lslB":  { INH: '58',                                                                     },
    "lsl":   {                           DIR: '08',   IDX: '68',   EXT: '78',                 },
    "lsrA":  { INH: '44',                                                                     },
    "lsrB":  { INH: '54',                                                                     },
    "lsr":   {                           DIR: '04',   IDX: '64',   EXT: '74',                 },
    "mul":   { INH: '3D',                                                                     },
    "negA":  { INH: '40',                                                                     },
    "negB":  { INH: '50',                                                                     },
    "neg":   {                           DIR: '00',   IDX: '60',   EXT: '70',                 },
    "nop":   { INH: '12',                                                                     },
    "orA":   {              IMM: '8A',   DIR: '9A',   IDX: 'AA',   EXT: 'BA',                 },
    "orB":   {              IMM: 'CA',   DIR: 'DA',   IDX: 'EA',   EXT: 'FA',                 },
    "orCC":  {              IMM: '1A',                                                        },
    "pshS":  {              IMM: '34',                                                        },
    "pshU":  {              IMM: '36',                                                        },
    "pulS":  {              IMM: '35',                                                        },
    "pulU":  {              IMM: '37',                                                        },
    "rolA":  { INH: '49',                                                                     },
    "rolB":  { INH: '59',                                                                     },
    "rol":   {                           DIR: '09',   IDX: '69',   EXT: '79',                 },
    "rorA":  { INH: '46',                                                                     },
    "rorB":  { INH: '56',                                                                     },
    "ror":   {                           DIR: '06',   IDX: '66',   EXT: '76',                 },
    "rti":   { INH: '3B',                                                                     },
    "rts":   { INH: '39',                                                                     },
    "sbcA":  {              IMM: '82',   DIR: '92',   IDX: 'A2',   EXT: 'B2',                 },
    "sbcB":  {              IMM: 'C2',   DIR: 'D2',   IDX: 'E2',   EXT: 'F2',                 },
    "sex":   { INH: '1D',                                                                     },
    "stA":   {                           DIR: '97',   IDX: 'A7',   EXT: 'B7',                 },
    "stB":   {                           DIR: 'D7',   IDX: 'E7',   EXT: 'F7',                 },
    "stD":   {                           DIR: 'DD',   IDX: 'ED',   EXT: 'FD',                 },
    "stS":   {                           DIR: '10DF', IDX: '10EF', EXT: '10FF',               },
    "stU":   {                           DIR: 'DF',   IDX: 'EF',   EXT: 'FF',                 },
    "stX":   {                           DIR: '9F',   IDX: 'AF',   EXT: 'BF',                 },
    "stY":   {                           DIR: '109F', IDX: '10AF', EXT: '10BF',               },
    "subA":  {              IMM: '80',   DIR: '90',   IDX: 'A0',   EXT: 'B0',                 },
    "subB":  {              IMM: 'C0',   DIR: 'D0',   IDX: 'E0',   EXT: 'F0',                 },
    "subD":  {              IMM: '83',   DIR: '93',   IDX: 'A3',   EXT: 'B3',                 },
    "swi":   { INH: '3F',                                                                     },
    "swi2":  { INH: '103F',                                                                   },
    "swi3":  { INH: '113F',                                                                   },
    "sync":  { INH: '13',                                                                     },
    "tfr":   {              INT: '1F',                                                        },
    "tstA":  { INH: '4D',                                                                     },
    "tstB":  { INH: '5D',                                                                     },
    "tst":   {                           DIR: '0D',   IDX: '6D',   EXT: '7D',                 },
}


OPCODES_6309 = {
    "bitMD": {              IMM: '113C'                                                       },
    "cmpr":  {              INT: '1037',                                                        },
    "decD":  { INH: '104A',                                                                     },
    "decE":  { INH: '114A',                                                                     },
    "decF":  { INH: '115A',                                                                     },
    "decW":  { INH: '105A',                                                                     },
    "incD":  { INH: '004C',                                                                     }, # !! LEADING ZEROS!
    "incE":  { INH: '014C',                                                                     },
    "incF":  { INH: '015C',                                                                     },
    "incW":  { INH: '005C',                                                                     },
    "ldE":   {              IMM: '0186',   DIR: '0196',   IDX: '01A6',   EXT: '01B6',         },
    "ldF":   {              IMM: '01C6',   DIR: '01D6',   IDX: '01E6',   EXT: '01F6',         },
    "ldQ":   {              IMM:   'CD',   DIR:   'DC',   IDX:   'EC',   EXT:   'FC',         },
    "ldW":   {              IMM:   '86',   DIR:   '96',   IDX:   'A6',   EXT:   'B6',         },
    "ldMD":  {              IMM: '113D',                                                      },
    "stE":   {                             DIR: '0197',   IDX: '01A7',   EXT: '01B7',         },
    "stF":   {                             DIR: '01D7',   IDX: '01E7',   EXT: '01F7',         },
    "stQ":   {                             DIR: '00DD',   IDX: '00ED',   EXT: '00FD',         },
    "stW":   {                             DIR: '0097',   IDX: '00A7',   EXT: '00B7',         },
}

OPCODES = {**OPCODES_6809, **OPCODES_6309}

# Used to interpret the unusual addressing modes of these instructions.
# From the programmers reference by Darren Atkinson:
#
#   "Unlike most other instructions which use the
#    Direct, Indexed and Extended addressing modes, the operand value used by the JMP instruction is
#    the Effective Address itself, rather than the memory contents stored at that address (unless
#    Indirect Indexing is used)."


# TODO: Handle these by adding an pseudo-addressing mode called Effective Addressing
JUMPS = {"JMP", "JSR"}
