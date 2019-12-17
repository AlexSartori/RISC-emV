import os, json
from riscemv.ISA.Instruction import Instruction


class Ret_Instruction(Instruction):
    rd_type = "int"


    def __init__(self):
        self.instr_name = 'ret'
        self.functional_unit = 'add'
        self.clock_needed = 1


    def to_binary(self):
        return '00000000000000001000000001100111'


    @staticmethod
    def parse(binary_code):
        return Ret_Instruction()


    def execute(self, rs1_value, rs2_value):
        return 1  # ra register


    def __str__(self):
        return 'ret'
