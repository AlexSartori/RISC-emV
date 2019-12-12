class ELF:
    def __init__(self, filename):
        self.file = open(filename, 'rb')
        print("ELF file:", self.file.name)

        self.eheader = {}
        self.parse_eh()  # ELF Header
        # for e in ['EI_CLASS', 'EI_DATA', 'e_machine', 'e_entry', 'e_phoff', 'e_shoff']:
        #     print("    {}: {}".format(e, self.eheader[e]))

        self.pheader = {}
        self.parse_ph()  # Program header

        self.sections = []
        self.parse_sh()  # Section header


    def __read_bytes__(self, n, to_int=True):
        data = self.file.read(n)

        if not to_int:
            return data
        elif 'EI_DATA' in self.eheader:
            return int.from_bytes(data, self.eheader['EI_DATA'])
        else:
            return int.from_bytes(data, 'little')


    def parse_eh(self):
        # Check magic number
        self.eheader['EI_MAG'] = self.__read_bytes__(4, to_int=False)
        if self.eheader['EI_MAG'] != b'\x7fELF':
            raise TypeError('Not al ELF file')
            return

        # Class (32 or 64 bit)
        self.eheader['EI_CLASS'] = '32' if self.__read_bytes__(1) == 1 else '64'

        # Endianness
        self.eheader['EI_DATA'] = 'little' if self.__read_bytes__(1) == 1 else 'big'
        self.eheader['EI_VERSION'] = self.__read_bytes__(1)    # 1 = original and current version
        self.eheader['EI_OSABI'] = self.__read_bytes__(1)      # 0 = System V
        self.eheader['EI_ABIVER'] = self.__read_bytes__(1)     # Further abi version
        self.eheader['EI_PAD'] = self.__read_bytes__(7)        # Unused
        self.eheader['e_type'] = self.__read_bytes__(2)        # Obj file type

        self.eheader['e_machine'] = self.__read_bytes__(2)     # Target ISA
        if self.eheader['e_machine'] != 243:
            raise TypeError("ELF.e_machine != RISC-V ({:x})".format(self.eheader['e_machine']))

        self.eheader['e_version'] = self.__read_bytes__(4)     # 1 = original and current

        if self.eheader['EI_CLASS'] == '32':                   # 4-byte address
            self.eheader['e_entry'] = self.__read_bytes__(4)   # Program entry point address
        else:
            self.eheader['e_entry'] = self.__read_bytes__(8)

        if self.eheader['EI_CLASS'] == '32':
            self.eheader['e_phoff'] = self.__read_bytes__(4)   # Program header offset
        else:
            self.eheader['e_phoff'] = self.__read_bytes__(8)

        if self.eheader['EI_CLASS'] == '32':
            self.eheader['e_shoff'] = self.__read_bytes__(4)   # Section header offset
        else:
            self.eheader['e_shoff'] = self.__read_bytes__(8)

        self.eheader['e_flags'] = self.__read_bytes__(4)       # Flags
        self.eheader['e_ehsize'] = self.__read_bytes__(2)      # This header's size
        self.eheader['e_phentsize'] = self.__read_bytes__(2)   # Size of a program header table entry
        self.eheader['e_phnum'] = self.__read_bytes__(2)       # Number of ph entries
        self.eheader['e_shentsize'] = self.__read_bytes__(2)   # Size of a section header table entry
        self.eheader['e_shnum'] = self.__read_bytes__(2)       # Number of sh entries
        self.eheader['e_shstrndx'] = self.__read_bytes__(2)    # Index of the sh table containing names


    def parse_ph(self):
        if self.eheader['e_phoff'] != 0:
            print("Parsing Program Header at {}: {}x{}".format(
                self.eheader['e_phoff'],
                self.eheader['e_phentsize'],
                self.eheader['e_phnum']
            ))

            raise NotImplementedError()

            # for i in range(int(self.eheader['e_phnum'])):
            #     entry = file.read(int(self.eheader['e_phentsize']))
            #     print(entry)
        else:
            print("Program Header not present")


    def parse_sh(self):
        print("Parsing Section Header at {}: {}x{}".format(
            self.eheader['e_shoff'],
            self.eheader['e_shentsize'],
            self.eheader['e_shnum']
        ))

        self.file.seek(self.eheader['e_shoff'])

        # Read section headers
        for i in range(int(self.eheader['e_shnum'])):
            self.sections.append(self.Section(self))

        # Read sections names
        strtab = ''
        for s in self.sections:
            if s.sh_type == 3:  # SHT_STRTAB
                print("    Found SHT_STRTAB at {} of {} bytes".format(s.sh_offset, s.sh_size))
                self.file.seek(s.sh_offset)
                data = self.file.read(s.sh_size)

                strtab = ''.join([chr(c) for c in data]) + strtab

        print("    .strtab: " + ''.join([c if c != '\0' else '_' for c in strtab]))

        # Assign names to sections
        for s in self.sections:
            name = ''
            idx = s.sh_name
            while strtab[idx] != '\0':
                name += strtab[idx]
                idx += 1

            print("        {} -> {}".format(s.sh_name, name))
            s.sh_name = name


    class Section:
        def __init__(self, elf):
            self.file = elf.file
            self.eheader = elf.eheader
            self.__read_bytes__ = elf.__read_bytes__

            self.sh_name = self.__read_bytes__(4)
            self.sh_type = self.__read_bytes__(4)

            if self.eheader['EI_CLASS'] == '32':
                self.sh_flags = self.__read_bytes__(4)
            else:
                self.sh_flags = self.__read_bytes__(8)

            if self.eheader['EI_CLASS'] == '32':
                self.sh_addr = self.__read_bytes__(4)
            else:
                self.sh_addr = self.__read_bytes__(8)

            if self.eheader['EI_CLASS'] == '32':
                self.sh_offset = self.__read_bytes__(4)
            else:
                self.sh_offset = self.__read_bytes__(8)

            if self.eheader['EI_CLASS'] == '32':
                self.sh_size = self.__read_bytes__(4)
            else:
                self.sh_size = self.__read_bytes__(8)

            self.sh_link = self.__read_bytes__(4)
            self.sh_info = self.__read_bytes__(4)

            if self.eheader['EI_CLASS'] == '32':
                self.sh_addralign = self.__read_bytes__(4)
            else:
                self.sh_addralign = self.__read_bytes__(8)

            if self.eheader['EI_CLASS'] == '32':
                self.sh_entsize = self.__read_bytes__(4)
            else:
                self.sh_entsize = self.__read_bytes__(8)

