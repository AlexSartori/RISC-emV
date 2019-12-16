from riscemv.ELF import ELF


elf = ELF("sample_programs/test_64.o")


def test_eheader():
    e = elf.eheader

    assert e['EI_MAG'] == b'\x7fELF', "Wrong magic number"
    assert e['EI_CLASS'] == '64'
    assert e['EI_DATA'] == 'little'
    assert e['e_machine'] == 243

    assert e['e_shoff'] == 504
    assert e['e_shstrndx'] == 8


def test_pheader():
    p = elf.pheader

    assert len(p) == 0  # Not present/implemented


def test_sheader():
    names = ['', '.text', '.data', '.bss', '.comment', '.riscv.attributes', '.symtab', '.strtab', '.shstrtab']

    for i, s in enumerate(elf.sections.values()):
        assert isinstance(s, ELF.Section)
        assert s.sh_name == names[i]
        # ...


def test_symtab():
    names = ['', 'test.c', '', '', '', '', '', 'main']

    for i, s in enumerate(elf.symbols):
        assert isinstance(s, ELF.Symbol)
        assert s.st_name == names[i]
