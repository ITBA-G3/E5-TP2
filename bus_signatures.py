from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out, Signature

class operand_b_regbank(wiring.Signature):
    def __init__(self):
        super().__init__({
            "rs1_data": Out(32),
            "rs2_data": Out(32)
        })
    
    def __eq__(self, other):
        return self.members == other.members
            
class alu_regbank(wiring.Signature):
    def __init__(self):
        super().__init__({            
            "rd_data": Out(32)
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
        
class operand_b_alu(wiring.Signature):
    def __init__(self):
        super().__init__({
            "A": Out(32),
            "B": Out(32)
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
    
class imm_data(wiring.Signature):
    def __init__(self):
        super().__init__({
            "imm": Out(32)
        })
    
    def __eq__(self, other):
        return self.members == other.members
    
class fetch_decode(wiring.Signature):
    def __init__(self):
        super().__init__({
            "instr": Out(32)
        })
    
    def __eq__(self, other):
        return self.members == other.members
    
class fetch_operand_b(wiring.Signature):
    def __init__(self):
        super().__init__({
            "pc" : Out(32)
        })
    
    def __eq__(self, other):
        return self.members == other.members
    
class operand_b_mux(wiring.Signature):
    def __init__(self):
        super().__init__({
            "muxA": Out(1),
                        # rs1   -> 0b0
                        # pc    -> 0b1
            "muxB": Out(3)
                        # rs2   -> 0b000
                        # immI  -> 0b001
                        # immU  -> 0b010
                        # immS  -> 0b011
                        # immB  -> 0b100
                        # immJ  -> 0b101
        })
    
    def __eq__(self, other):
        return self.members == other.members
    

class addrbuilder_enable(wiring.Signature):
    def __init__(self):
        super().__init__({
            "enable": In(1)  # Enable signal for the addrbuilder
        })
    
    def __eq__(self, other):
        return self.members == other.members
    
class pc_update(wiring.Signature):
    def __init__(self):
        super().__init__({
            "pc": Out(32)
        })
    
    def __eq__(self, other):
        return self.members == other.members

class branch_flags(wiring.Signature):
    def __init__(self):
        super().__init__({
            "beq": Out(1),
            "bne": Out(1),
            "blt": Out(1),
            "bge": Out(1),
            "bltu": Out(1),
            "bgeu": Out(1)
        })
    
    def __eq__(self, other):
        return self.members == other.members

class data_uart(wiring.Signature):
    def __init__(self):
        super().__init__({
            "data" : Out(32)
        })
    
    def __eq__(self, other):
        return self.members == other.members

class start_uart(wiring.Signature):
    def __init__(self):
        super().__init__({
            "start" : Out(1)
        })
    
    def __eq__(self, other):
        return self.members == other.members

class tx_uart(wiring.Signature):
    def __init__(self):
        super().__init__({
            "tx" : Out(1)
        })
    
    def __eq__(self, other):
        return self.members == other.members

class ready_uart(wiring.Signature):
    def __init__(self):
        super().__init__({
            "ready" : Out(1)
        })
    
    def __eq__(self, other):
        return self.members == other.members
            
            