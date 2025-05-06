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
            