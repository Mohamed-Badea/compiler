# documentation.py

# SIC/XE Instruction Set with format and opcode

class Documentation:
    PROG_NAME = ""

    INSTRUCTIONS = {
        'ADD':   {'format': 3, 'opcode': '18'},
        'ADDF':  {'format': 3, 'opcode': '58'},
        'ADDR':  {'format': 2, 'opcode': '90'},
        'AND':   {'format': 3, 'opcode': '40'},
        'CLEAR': {'format': 2, 'opcode': 'B4'},
        'COMP':  {'format': 3, 'opcode': '28'},
        'COMPF': {'format': 3, 'opcode': '88'},
        'COMPR': {'format': 2, 'opcode': 'A0'},
        'DIV':   {'format': 3, 'opcode': '24'},
        'DIVF':  {'format': 3, 'opcode': '64'},
        'DIVR':  {'format': 2, 'opcode': '9C'},
        'FIX':   {'format': 1, 'opcode': 'C4'},
        'FLOAT': {'format': 1, 'opcode': 'C0'},
        'HIO':   {'format': 1, 'opcode': 'F4'},
        'J':     {'format': 3, 'opcode': '3C'},
        'JEQ':   {'format': 3, 'opcode': '30'},
        'JGT':   {'format': 3, 'opcode': '34'},
        'JLT':   {'format': 3, 'opcode': '38'},
        'JSUB':  {'format': 3, 'opcode': '48'},
        'LDA':   {'format': 3, 'opcode': '00'},
        'LDB':   {'format': 3, 'opcode': '68'},
        'LDCH':  {'format': 3, 'opcode': '50'},
        'LDF':   {'format': 3, 'opcode': '70'},
        'LDL':   {'format': 3, 'opcode': '08'},
        'LDS':   {'format': 3, 'opcode': '6C'},
        'LDT':   {'format': 3, 'opcode': '74'},
        'LDX':   {'format': 3, 'opcode': '04'},
        'MUL':   {'format': 3, 'opcode': '20'},
        'MULF':  {'format': 3, 'opcode': '60'},
        'MULR':  {'format': 2, 'opcode': '98'},
        'NORM':  {'format': 1, 'opcode': 'C8'},
        'OR':    {'format': 3, 'opcode': '44'},
        'RD':    {'format': 3, 'opcode': 'D8'},
        'RMO':   {'format': 2, 'opcode': 'AC'},
        'RSUB':  {'format': 3, 'opcode': '4C'},
        'SHIFTL':{'format': 2, 'opcode': 'A4'},
        'SHIFTR':{'format': 2, 'opcode': 'A8'},
        'SIO':   {'format': 1, 'opcode': 'F0'},
        'STA':   {'format': 3, 'opcode': '0C'},
        'STB':   {'format': 3, 'opcode': '78'},
        'STCH':  {'format': 3, 'opcode': '54'},
        'STF':   {'format': 3, 'opcode': '80'},
        'STI':   {'format': 3, 'opcode': 'D4'},
        'STL':   {'format': 3, 'opcode': '14'},
        'STS':   {'format': 3, 'opcode': '7C'},
        'STSW':  {'format': 3, 'opcode': 'E8'},
        'STT':   {'format': 3, 'opcode': '84'},
        'STX':   {'format': 3, 'opcode': '10'},
        'SUB':   {'format': 3, 'opcode': '1C'},
        'SUBF':  {'format': 3, 'opcode': '5C'},
        'SUBR':  {'format': 2, 'opcode': '94'},
        'SVC':   {'format': 2, 'opcode': 'B0'},
        'TD':    {'format': 3, 'opcode': 'E0'},
        'TIO':   {'format': 1, 'opcode': 'F8'},
        'TIX':   {'format': 3, 'opcode': '2C'},
        'TIXR':  {'format': 2, 'opcode': 'B8'},
        'WD':    {'format': 3, 'opcode': 'DC'},
        #Phase2
        'PADD': {'format': '3X', 'opcode': 'BC'},
        'PSUB': {'format': '3X', 'opcode': '8C'},
        'PMUL': {'format': '3X', 'opcode': 'E4'},
        'PDIV': {'format': '3X', 'opcode': 'FC'},
        'PMOV': {'format': '3X', 'opcode': 'CC'},
    }

# Assembler Directives
    DIRECTIVES = ['START', 'END', 'BYTE', 'WORD', 'RESB', 'RESW', 'BASE', 'NOBASE', 'EQU', 'ORG', 'LTORG']

# Format size in bytes
    FORMAT_SIZE = {
    1: 1,
    2: 2,
    3: 3,
    4: 4
}

# Registers used in format 2
    REGISTERS = {
    'A': 0,
    'X': 1,
    'L': 2,
    'B': 3,
    'S': 4,
    'T': 5,
    'F': 6,
    'PC': 8,
    'SW': 9
}

    def is_instruction(self, opcode): # T or F
        return opcode in self.INSTRUCTIONS

    def is_directive(self, opcode): # T of F
        return opcode in self.DIRECTIVES

    def get_format(self, opcode): # int
        if opcode in self.INSTRUCTIONS:
            return self.INSTRUCTIONS[opcode]['format']
        return None

    @classmethod
    def set_prog_name(self, name):
        self.PROG_NAME = name

    @classmethod
    def get_prog_name(self):
        if self.PROG_NAME == "":
            return "Program name is empty!"
        return self.PROG_NAME
