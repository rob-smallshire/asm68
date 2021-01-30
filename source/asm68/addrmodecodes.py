INH = "Inherent"           # The 'address' is inherent in the opcode. e.g. ABX
INT = "Interregister"      # An pseudo-addressing for an immediate operand which specified registers for the EXG and TFR instructions
IMM = "Immediate"          # Operand immediately follows the opcode. A literal. Could be 8-bit (LDA), 16-bit (LDD), or 32-bit (LDQ)
DIR = "PageDirect"         # An 8-bit offset pointer from the base of the direct page, as defined by the DP register. Also known as just 'Direct'.
IDX = "Indexed"            # Relative to the address in a base register (an index register or stack pointer)
EXT = "ExtendedDirect"     # A 16-bit pointer to a memory location. Also known as just 'Extended'.
REL8 = "Relative8 8-bit"   # Program counter relative
REL16 = "Relative8 16-bit" # Program counter relative

# What about what Leventhal calls 'Register Addressing'. e.g. EXG X,U