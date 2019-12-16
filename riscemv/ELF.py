from riscemv.ISA.ISA import ISA
from riscemv.ISA.IType_Instruction import IType_Instruction
from riscemv.ISA.UType_Instruction import UType_Instruction
from riscemv.ISA.UJType_Instruction import UJType_Instruction


class ELF:
    def __init__(self, filename):
        self.file = open(filename, 'rb')
        print("Parsing ELF file:", self.file.name)

        self.symbols = []

        self.eheader = {}
        self.parse_eh()  # ELF Header

        self.pheader = {}
        self.parse_ph()  # Program header

        self.sections = []
        self.parse_sh()  # Section header


    def load_program(self, prog):
        print("\nLoading program into memory...")
        next_addr = 0  # If file is relocatable, need to store sections one after the other

        for s in self.sections.values():
            if s.sh_type == 0:  # SHT_NULL
                continue

            print("    {}:".format(s.sh_name))

            # Load in memory
            if s.sh_flags & 0x02 != 0x02:
                print("        ! SHF_ALLOC flag not set, skipping")
                continue
            if s.sh_addr == 0 and self.eheader['e_type'] != 1:  # Not ET_REL (relocatable)
                print("        ! sh_addr is set to 0 and file is not relocatable, skipping")
                continue
            if s.sh_addr == 0:
                s.sh_addr = next_addr
            if s.sh_type == 8:  # SHT_NOBITS, like .bss, doesn't have content
                print("        - sh_type is set to SHT_NOBITS, setting {} bytes to 0x00".format(s.sh_size))
                for offset in range(s.sh_size):
                    prog.DM.store(s.sh_addr + offset, 0x00)
            else:
                self.file.seek(s.sh_offset)
                s.content = self.file.read(s.sh_size)
                for offset, byte in enumerate(s.content):
                    prog.DM.store(s.sh_addr + offset, byte)

            print("        > Loaded {} bytes from {} to {} excluded. (Read from offset {})".format(
                s.sh_size, s.sh_addr, s.sh_addr + s.sh_size, s.sh_offset
            ))
            next_addr += s.sh_size

            # Insert start address in program's section array
            prog.sections[s.sh_name] = s.sh_addr

        # Dump DM
        print("\nData Memory dump (first 128 bytes):")
        bin, hex, ascii = [], [], []
        for addr, val in enumerate(prog.DM):
            if addr >= 128:
                break
            bin.append('{:08b}'.format(val))
            hex.append('{:02x}'.format(val))
            ascii.append(chr(val) if chr(val).isprintable() and chr(val) != '\n' else '.')

        bin_idx, hex_idx, ascii_idx = 0, 0, 0
        while bin_idx < len(bin):
            print('   ', ' '.join(bin[bin_idx:bin_idx+8]), end=' │ ')
            bin_idx += 8
            print(' '.join(hex[hex_idx:hex_idx+8]), end=' │ ')
            hex_idx += 8
            print(''.join(ascii[ascii_idx:ascii_idx+8]))
            ascii_idx += 8

        # Make relocation of symbols
        symbol_bindings = self.parse_rs()  # Relocation section

        # Parse .text section to instructions
        print("\nParsing .text section into ISA.Instruction objects...")
        isa = ISA()
        pc = prog.sections['.text']
        self.file.seek(self.sections['.text'].sh_offset)


        while self.file.tell() < self.sections['.text'].sh_offset + self.sections['.text'].sh_size:
            bin = ["{:08b}".format(b) for b in reversed(self.file.read(4))]

            bin = ''.join(''.join((byte)) for byte in bin)

            try:
                inst = isa.instruction_from_bin(bin, pc)
            except:
                inst = None

            if symbol_bindings is not None and len(prog.IM) in symbol_bindings:  # Relocate symbol in the instruction
                sym = symbol_bindings[len(prog.IM)]
                print("    (relocating a symbol: {})".format(sym))
                if isinstance(inst, (IType_Instruction, UType_Instruction, UJType_Instruction)):
                    inst.imm = sym

            print('   ', bin, '->', inst if inst is not None else "! [error]")
            if inst is not None:
                prog.IM.append(inst)


    def __read_bytes__(self, n, to_int=True):
        data = self.file.read(n)

        if not to_int:
            return data
        elif 'EI_DATA' in self.eheader:
            return int.from_bytes(data, self.eheader['EI_DATA'])
        else:
            return int.from_bytes(data, 'little')


    def parse_rs(self):
        print("\nParsing .rela.text section...")
        if '.rela.text' not in self.sections:
            print("    Not present")
            return None

        binding = {}

        self.file.seek(self.sections['.rela.text'].sh_offset)
        while self.file.tell() < self.sections['.rela.text'].sh_offset + self.sections['.rela.text'].sh_size:
            relo = self.Relocation(self)
            
            symbol = self.symbols[relo.r_info_sym_num]
            offset = relo.r_offset / 4

            if relo.r_info_type == 26:  # %hi
                binding[offset] = '%hi({})'.format(symbol.st_name)
            elif relo.r_info_type == 27:  # %lo
                binding[offset] = '%lo({})'.format(symbol.st_name)

        return binding


    def parse_eh(self):
        # Check magic number
        self.eheader['EI_MAG'] = self.__read_bytes__(4, to_int=False)
        if self.eheader['EI_MAG'] != b'\x7fELF':
            raise TypeError('Not al ELF file')

        # Class (32 or 64 bit)
        self.eheader['EI_CLASS'] = '32' if self.__read_bytes__(1) == 1 else '64'

        # Endianness
        self.eheader['EI_DATA']     = 'little' if self.__read_bytes__(1) == 1 else 'big'
        self.eheader['EI_VERSION']  = self.__read_bytes__(1)   # 1 = original and current version
        self.eheader['EI_OSABI']    = self.__read_bytes__(1)   # 0 = System V
        self.eheader['EI_ABIVER']   = self.__read_bytes__(1)   # Further abi version
        self.eheader['EI_PAD']      = self.__read_bytes__(7)   # Unused
        self.eheader['e_type']      = self.__read_bytes__(2)   # Obj file type

        self.eheader['e_machine']   = self.__read_bytes__(2)   # Target ISA
        if self.eheader['e_machine'] != 243:
            raise TypeError("ELF.e_machine != RISC-V ({:x})".format(self.eheader['e_machine']))

        self.eheader['e_version']   = self.__read_bytes__(4)   # 1 = original and current

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

        self.eheader['e_flags']     = self.__read_bytes__(4)   # Flags
        self.eheader['e_ehsize']    = self.__read_bytes__(2)   # This header's size
        self.eheader['e_phentsize'] = self.__read_bytes__(2)   # Size of a program header table entry
        self.eheader['e_phnum']     = self.__read_bytes__(2)   # Number of ph entries
        self.eheader['e_shentsize'] = self.__read_bytes__(2)   # Size of a section header table entry
        self.eheader['e_shnum']     = self.__read_bytes__(2)   # Number of sh entries
        self.eheader['e_shstrndx']  = self.__read_bytes__(2)   # Index of the sh table containing names


    def parse_ph(self):
        print("\nParsing Program Header at {}: {}x{}".format(
            self.eheader['e_phoff'],
            self.eheader['e_phentsize'],
            self.eheader['e_phnum']
        ))

        if self.eheader['e_phoff'] != 0:
            raise NotImplementedError()

            # for i in range(int(self.eheader['e_phnum'])):
            #     entry = file.read(int(self.eheader['e_phentsize']))
            #     print(entry)
        else:
            print("    Program Header not present")


    def parse_sh(self):
        print("\nParsing Section Header at {}: {}x{}".format(
            self.eheader['e_shoff'],
            self.eheader['e_shentsize'],
            self.eheader['e_shnum']
        ))

        self.file.seek(self.eheader['e_shoff'])

        # Read section headers
        for i in range(int(self.eheader['e_shnum'])):
            self.sections.append(self.Section(self))

        # Read sections names
        shstrtab_sec = self.sections[self.eheader['e_shstrndx']]
        self.file.seek(shstrtab_sec.sh_offset)
        data = self.file.read(shstrtab_sec.sh_size)
        shstrtab = ''.join([chr(c) for c in data])

        # Assign sections names
        named_sections = {}
        for s in self.sections:
            name = ''
            idx = s.sh_name
            while shstrtab[idx] != '\0':
                name += shstrtab[idx]
                idx += 1

            s.sh_name = name
            named_sections[name] = s
            print("    {}: {} bytes".format(s.sh_name, s.sh_size))
        self.sections = named_sections

        # Read strings section
        strtab = self.sections['.strtab']
        self.file.seek(strtab.sh_offset)
        data = self.file.read(strtab.sh_size)
        strtab.content = ''.join([chr(c) for c in data])

        print("\nReading symbol table...")

        # Load symbol table
        symtab = self.sections['.symtab']
        self.file.seek(symtab.sh_offset)
        symtab.content = []
        while self.file.tell() < symtab.sh_offset + symtab.sh_size:
            sym = self.Symbol(self)

            # Assign name from .strtab
            name = ''
            idx = sym.st_name
            while strtab.content[idx] != '\0':
                name += strtab.content[idx]
                idx += 1
            sym.st_name = name
            self.symbols.append(sym)

            if name != '':
                print("    {} := {}".format(sym.st_name, sym.st_value))


    class Symbol:
        def __init__(self, elf):
            self.file = elf.file
            self.eheader = elf.eheader
            self.__read_bytes__ = elf.__read_bytes__

            self.st_name = self.__read_bytes__(4)
            if self.eheader['EI_CLASS'] == '32':
                self.st_value = self.__read_bytes__(4, to_int=False)
            else:
                self.st_value = self.__read_bytes__(8, to_int=False)

            if self.eheader['EI_CLASS'] == '32':
                self.st_size = self.__read_bytes__(4)
            else:
                self.st_size = self.__read_bytes__(8)

            self.st_info = self.__read_bytes__(1, to_int=False)
            self.st_other = self.__read_bytes__(1, to_int=False)
            self.st_half = self.__read_bytes__(2, to_int=False)


    class Section:
        def __init__(self, elf):
            self.file = elf.file
            self.eheader = elf.eheader
            self.__read_bytes__ = elf.__read_bytes__
            self.content = None

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


    class Relocation:
        def __init__(self, elf):
            self.file = elf.file
            self.eheader = elf.eheader
            self.__read_bytes__ = elf.__read_bytes__

            if self.eheader['EI_CLASS'] == '32':
                self.r_offset = self.__read_bytes__(4)
            else:
                self.r_offset = self.__read_bytes__(8)

            if self.eheader['EI_CLASS'] == '32':
                self.r_info_type = self.__read_bytes__(1)
                self.r_info_sym_num = self.__read_bytes__(3)
                #self.r_info = self.__read_bytes__(4, to_int=False)
            else:
                self.r_info_type = self.__read_bytes__(4)
                self.r_info_sym_num = self.__read_bytes__(4)
                #self.r_info = self.__read_bytes__(8, to_int=False)

            if self.eheader['EI_CLASS'] == '32':
                self.r_addend = self.__read_bytes__(4)
            else:
                self.r_addend = self.__read_bytes__(8)
