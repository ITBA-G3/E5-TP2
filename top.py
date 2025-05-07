from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out, connect
from amaranth_boards import arty_a7

from regbank import RegBank
from alu import ALU
from decoder import Decoder
from fetch import Fetch
from opbuilder import opBuilder

class Top (Elaboratable):
    def __init__(self):
        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.submodules.regbank = regbank = RegBank()
        m.submodules.alu = alu = ALU()
        m.submodules.decoder = decoder = Decoder()
        m.submodules.fetch = fetch = Fetch()
        m.submodules.opbuilder = opbuilder = opBuilder()
        
        self.alu = alu
        self.regbank = regbank
        self.decoder = decoder
        self.fetch = fetch
        self.opbuilder = opbuilder

        connect(m, regbank.rd_bus, alu.rd_bus)
        connect(m, decoder.alu_flags, alu.flags_in)
        connect(m, decoder.reg_addr, regbank.reg_addr)
        connect(m, decoder.functions, alu.functions)
        connect(m, fetch.pc, opbuilder.pc)
        connect(m, fetch.instr, decoder.instr)
        connect(m, opbuilder.data_regbank, regbank.rs_buses)
        connect(m, opbuilder.alu_buses, alu.data_buses)
        connect(m, opbuilder.imm, decoder.imm_data)

        return m