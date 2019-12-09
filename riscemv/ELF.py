class ELF:
    def __init__(self, filename):
        self.file = open(filename, 'rb')
        print("ELF file:", filename)

        self.eheader = {}
        self.parse_eh(self.file)  # ELF Header
        for e in ['EI_CLASS', 'EI_DATA', 'e_machine', 'e_entry', 'e_phoff', 'e_shoff']:
            print("    {}: {}".format(e, self.eheader[e]))

        self.parse_ph(self.file)  # Program header

    def parse_eh(self, file):
        # Check magic number
        self.eheader['EI_MAG'] = file.read(4)
        if self.eheader['EI_MAG'] != b'\x7fELF':
            raise TypeError('Not al ELF file')
            return

        self.eheader['EI_CLASS'] = file.read(1)      # 1 = 32bit   2 = 64bit
        self.eheader['EI_DATA'] = file.read(1)       # 1 = little  2 = big
        self.eheader['EI_VERSION'] = file.read(1)    # 1 = original and current version
        self.eheader['EI_OSABI'] = file.read(1)      # 0 = System V
        self.eheader['EI_ABIVER'] = file.read(1)     # Further abi version
        self.eheader['EI_PAD'] = file.read(7)        # Unused
        self.eheader['e_type'] = file.read(2)        # Obj file type

        self.eheader['e_machine'] = file.read(2)     # Target ISA
        if self.eheader['e_machine'] != b'\xf3\x00':
            raise TypeError("ELF.e_machine != RISC-V ({})".format(self.eheader['e_machine']))

        self.eheader['e_version'] = file.read(4)     # 1 = original and current

        if self.eheader['EI_CLASS'] == '1':          # 4-byte address
            self.eheader['e_entry'] = file.read(4)   # Program entry point address
        else:
            self.eheader['e_entry'] = file.read(8)

        if self.eheader['EI_CLASS'] == '1':
            self.eheader['e_phoff'] = file.read(4)   # Program header offset
        else:
            self.eheader['e_phoff'] = file.read(8)

        if self.eheader['EI_CLASS'] == '1':
            self.eheader['e_shoff'] = file.read(4)   # Section header offset
        else:
            self.eheader['e_shoff'] = file.read(8)

        self.eheader['e_flags'] = file.read(4)       # Flags
        self.eheader['e_ehsize'] = file.read(2)      # This header's size
        self.eheader['e_phentsize'] = file.read(2)   # Size of a program header table entry
        self.eheader['e_phnum'] = file.read(2)       # Number of ph entries
        self.eheader['e_shentsize'] = file.read(2)   # Size of a section header table entry
        self.eheader['e_shnum'] = file.read(2)       # Number of sh entries
        self.eheader['e_shstrndx'] = file.read(2)    # Index of the sh table containing names


    def parse_ph(self, file):
        pass
