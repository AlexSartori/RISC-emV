import os
from riscemv.ProgramLoader import ProgramLoader



# def test_asm_to_binary():
#     PL = ProgramLoader(32)
#     inst = "add r3, r0, r1"
#     exp = "00000000000100000000000110110011"
#
#     assert PL.asm_to_binary(inst) == exp


# def test_load_assembly_code():
#     PL = ProgramLoader(32)
#     f = os.path.join(os.path.dirname(__file__), "..", "sample_programs", "_test1.s")
#     exp = [
#         '00000000000100010000000110110011',
#         '00000000011000101110001000110011',
#         '01000000010000011000000100110011'
#     ]
#     PL.load_assembly_code(open(f).read())
#
#     assert PL.lines == exp
