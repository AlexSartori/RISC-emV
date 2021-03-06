import re
from riscemv.ISA.ISA import ISA
from riscemv.ELF import ELF


class Program:
    def __init__(self, DM):
        self.DM = DM
        self.ISA = ISA()

        self.syntax_errors = []         # Line numbers for text
        self.unknown_instructions = []  # Instruction indexes for ELF

        self.IM = []  # Instruction Memory
        self.sections = {'.text': 0}
        self.symbol_table = {}
        self.alignment = 4
        self.directives = {
            '.byte':  1,
            '.2byte': 2,
            '.4byte': 4,
            '.8byte': 8,
            '.half':  2,
            '.word':  4,
            '.dword': 8,
            # '.asciz': None,
            # '.string': None,
            # '.zero': None
        }


    def get_entry_point(self):
        if '_start' in self.symbol_table:
            return self.symbol_table['_start']['value']
        elif 'main' in self.symbol_table:
            return self.symbol_table['main']['value']
        else:
            return self.sections['.text']


    def load_text(self, text):
        pc = 0
        for l_n, line in enumerate(text.split('\n')):
            line = line.split(';')[0].strip()
            line = line.replace('\t', ' ')

            if line != '':
                if re.match(r'.+:', line):
                    # Label
                    label = re.match(r'.+:', line).group(0)
                    label = label[:-1].lower()
                    self.symbol_table[label] = {
                        'name': label,
                        'value': pc,
                        'size': 0,
                        'section': '.text'
                    }
                    self.last_symbol = label
                elif re.match(r'\.[a-zA-Z0-9]+', line):
                    # Directive
                    try:
                        pc = self.__parse_directive__(line, pc)
                    except SyntaxError as s:
                        self.syntax_errors.append((l_n, line, s))
                else:
                    # Instruction
                    try:
                        inst = self.ISA.instruction_from_str(line, self.symbol_table, pc)
                        self.IM.append(inst)

                        # Load 32 bits into memory
                        for i in range(4):
                            self.DM.store(pc+i, int(inst.to_binary()[8*i:(8*i)+8], 2))
                    except NotImplementedError:
                        self.syntax_errors.append((l_n, line, "Instruction not yet implemented"))
                    except SyntaxError:
                        self.syntax_errors.append((l_n, line, "Unknown instruction"))

                    pc += 4


    def __parse_directive__(self, line, pc):
        line = line.split(' ')

        sections = ['.text', '.data', '.rodata', '.bss']
        if line[0] in sections or (line[0] == '.section' and line[1]) in sections:
            section = line[0] if line[0] in sections else line[1]
            self.sections[section] = pc
        elif line[0] == '.align' or line[0] == '.p2align':
            self.alignment = 2**int(line[1])
        elif line[0] == '.balign':
            self.alignment = int(line[1])
        elif line[0] in self.directives:
            # TODO: store value byte per byte
            dir = self.directives[line[0]]
            val = line[1]

            for offset in range(self.alignment):
                self.DM.store(pc, val)
        elif line[0] == '.zero':
            addr = pc
            while addr < int(line[1]):
                self.DM.store(addr, 0)
                addr += 1
            pc += addr
        elif line[0] == '.string' or line[0] == '.asciz':
            s = line[1][1:-1]  # Remove quotes
            addr = pc

            for c in s:
                self.DM.store(addr, ord(c))
                addr += 1

            pc += addr
        else:
            raise SyntaxError("Unknown directive")

        return pc


    def __iter__(self):
        return iter(self.IM)


    def load_machine_code(self, filename):
        file = ELF(filename)
        file.load_program(self)
        self.unknown_instructions = file.unknown_instructions


    def to_code(self):
        lines = []
        done_sections = []

        for idx, inst in enumerate(self.IM):
            for s in self.sections:
                if self.sections[s] == idx*4:
                    if s != '.text':  # If not the first line
                        lines.append('')
                    lines.append(s)
                    done_sections.append(s)
            for s in self.symbol_table:
                if self.symbol_table[s]['value'] == idx*4 and self.symbol_table[s]['section'] == done_sections[-1]:
                    lines.append('')
                    lines.append(s + ':')
            lines.append('    ' + str(inst))

            if idx in self.unknown_instructions:
                self.syntax_errors.append((len(lines)-1, str(inst), "Unknown Instruction"))

        for s in self.sections:
            if s not in done_sections:
                lines.append('')
                lines.append(s)
                for sym in self.symbol_table.values():
                    if sym['section'] == s:
                        lines.append(sym['name'] + ":")

                        if sym['size'] == 1:
                            dim = '.byte'
                        elif sym['size'] == 2:
                            dim = '.2byte'
                        elif sym['size'] == 4:
                            dim = '.4byte'
                        elif sym['size'] == 8:
                            dim = '.8byte'
                        else:
                            lines.append('    <no_info>')
                            continue

                        data = []
                        for i in range(sym['size']):
                            addr = self.sections[sym['section']] + sym['value']
                            data.append('{:x}'.format(self.DM.load(addr)))

                        lines.append("    {} 0x{}".format(dim, ''.join(data)))

        return '\n'.join(lines)
