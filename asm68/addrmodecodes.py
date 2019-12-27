INH = "Inherent"           # The 'address' is inherent in the opcode. e.g. ABX
IMM = "Immediate"          # Operand immediately follows the opcode. A literal. Could be 8-bit (LDA), 16-bit (LDD), or 32-bit (LDQ)
DIR = "Direct"             # An 8-bit offset pointer from the base of the direct page, as defined by the DP register.
IDX = "Indexed"            # Relative to the address in a base register (an index register or stack pointer)
EXT = "Extended"           # A 16-bit pointer to a memory location
REL8 = "Relative8 8-bit"   # Program counter relative
REL16 = "Relative8 16-bit" # Program counter relative

# What about what Leventhal calls 'Register Addressing'. e.g. EXG X,U