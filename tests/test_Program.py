import os
from riscemv.Program import Program
from riscemv.DataMemory import DataMemory


def test_load_text():
    image = '18 02 49 01 90 02 89 01 00 94 8c 63 00 95 24 23 42 92 c1 01 00 a4 86 33'
    image = image.split(' ')

    DM = DataMemory(128)
    p = Program(DM)

    p.load_text(open("sample_programs/_beq.s", 'r').read())

    for i, v in enumerate((DM)):
        if i == len(image):
            break
        else:
            assert '{:02x}'.format(v) == image[i], "Data memory differs at byte " + str(i)


def test_load_elf():
    image = '13 01 01 fe 23 2e 81 00 13 04 01 02 93 07 a0 00 23 26 f4 fe 93 07 c0 00 23 24 f4 fe 03 27 c4 fe 83 27 84 fe b3 07 f7 00 23 22 f4 fe 93 07 00 00 13 85 07 00 03 24 c1 01 13 01 01 02 67 80'
    image = image.split(' ')

    DM = DataMemory(128)
    p = Program(DM)

    p.load_machine_code("sample_programs/test_32.o")

    for i, v in enumerate((DM)):
        if i == len(image):
            break
        else:
            assert '{:02x}'.format(v) == image[i], "Data memory differs at byte " + str(i)
