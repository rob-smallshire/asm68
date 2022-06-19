asm68 - A Python-based assembler for 6809 and 6309 microprocessors
==================================================================

This package implements an *embedded domain-specific-language* in
Python for representing Motorola 6809 or Hitachi 6309 assembly code,
together with a assembler to machine code.

Status
======

The assembler is currently in development.

Build status:

.. image:: https://coveralls.io/repos/github/rob-smallshire/asm68/badge.svg?branch=master
    :target: https://coveralls.io/github/rob-smallshire/asm68?branch=master

Example
=======

Example use of the embedded assembly syntax::

    from asm68.asmdsl import AsmDsl, statements
    from asm68.assembler import assemble
    from asm68.mnemonics import (LDB, LDX, LDA, STA, SWI, ORG, FCB)
    from asm68.registers import X

    asm = AsmDsl()
    asm         (   LDB,    {0x41},     "GET DATA"                  )
    asm         (   LDX,    asm.SQTAB,  "GET BASE ADDRESS"          )
    asm         (   LDA,    {B:X},      "GET SQUARE OF DATA"        )
    asm         (   STA,    {0x42},     "STORE SQUARE"              )
    asm         (   SWI                                             )
    asm         (   ORG,    0x50,       "TABLE OF SQUARES"          )
    asm .SQTAB  (   FCB,    (0, 1, 4, 9, 16, 25, 36, 49)            )

    code = assemble(statements(asm))

The resulting ``code`` object will be a dictionary mapping of integer
addresses to contiguous blocks of code or data representes as bytes
objects.


Origin
======

This work started out as a fork of Craig Thomas's (GitHub @craigthomas)
https://github.com/craigthomas/CoCo3Assembler but rapidly diverged
to pursue it's own goals and the only vestige of the original code is
the opcode table, which even so is somewhat modified.
