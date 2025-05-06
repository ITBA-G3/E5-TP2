from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out, connect
from amaranth_boards import arty_a7

from regbank import RegBank
from alu import ALU
from decoder import Decoder

class Top (Elaboratable):
    def __init__(self):
        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.submodules.regbank = regbank = RegBank()
        m.submodules.alu = alu = ALU()
        m.submodules.decoder = decoder = Decoder()
        
        self.alu = alu
        self.regbank = regbank
        self.decoder = decoder

        connect(m, regbank.reg_buses, alu.alu_buses)
        connect(m, decoder.alu_flags, alu.flags_in)
        connect(m, decoder.reg_addr, regbank.reg_addr)
        connect(m, decoder.functions, alu.functions)
        # connect(m, decoder.imm_data, alu.imm_data) #TODO: Aún no lo tenemos

        return m