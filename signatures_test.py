from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out, Signature

class alu_regbank(wiring.Signature):
    def __init__(self):
        super().__init__({
            "rs1_data": Out(32),
            "rs2_data": Out(32),
            "rd_data": In(32)
        })
    
    def __eq__(self, other):
        return self.members == other.members
            
class decode_alu_flags(wiring.Signature):
    def __init__(self):
        super().__init__({
            "isALUreg": Out(1),
            "isALUimm": Out(1),
            "isBranch": Out(1),
            "isJALR": Out(1),
            "isJAL": Out(1),
            "isAUIPC": Out(1),
            "isLUI": Out(1),
            "isLoad": Out(1),
            "isStore": Out(1)
        })
    
    def __eq__(self, other):
        return self.members == other.members
    
class decode_reg_addr(wiring.Signature):
    def __init__(self):
        super().__init__({
            "rs1_addr": Out(5),
            "rs2_addr": Out(5),
            "rd_addr": Out(5)
        })
    
    def __eq__(self, other):
        return self.members == other.members

class decode_alu_fun(wiring.Signature):
    def __init__(self):
        super().__init__({
            "func3": Out(3),
            "func7": Out(7)
            # "shamt": Out(5)
        })
    
    def __eq__(self, other):
        return self.members == other.members
    
class decode_imm(wiring.Signature):
    def __init__(self):
        super().__init__({
            "Iimm": Out(32),
            "Uimm": Out(32),
            "Simm": Out(32),
            "Bimm": Out(32),
            "Jimm": Out(32)
        })
    
    def __eq__(self, other):
        return self.members == other.members