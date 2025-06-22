from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out, connect
from amaranth_boards import arty_a7

from regbank import RegBank
from alu import ALU
from decoder import Decoder
from fetch import Fetch
from opbuilder import opBuilder
# from immbuilder import Immbuilder
# from addrbuilder_jmpctrl import addrbuilder
from Amaranth.Modules.Latches.decode_latch import Decode_latch
from Amaranth.Modules.Latches.execute_latch import Execute_latch

class Top (Elaboratable):
    def __init__(self):
        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.submodules.regbank = regbank = RegBank()
        m.submodules.decode_latch = decode_latch = Decode_latch()
        m.submodules.execute_latch = execute_latch = Execute_latch()
        m.submodules.alu = alu = ALU()
        m.submodules.decoder = decoder = Decoder()
        m.submodules.fetch = fetch = Fetch()
        m.submodules.opbuilder = opbuilder = opBuilder()
        # m.submodules.imm_builder = imm_builder = Immbuilder()
        # m.submodules.addr_builder = addr_builder = addrbuilder()
        
        self.decode_latch = decode_latch
        self.execute_latch = execute_latch
        self.alu = alu
        self.regbank = regbank
        self.decoder = decoder
        self.fetch = fetch
        self.opbuilder = opbuilder
        # self.imm_builder = imm_builder
        # self.addr_builder = addr_builder

        # Fetch outputs
        connect(m, fetch.pc, decode_latch.pc_in)
        connect(m,fetch.instr, decoder.instr)
        # connect(m, fetch.instr, imm_builder.instr)
        
        # Imm builder outputs
        # connect(m, imm_builder.immdata, decode_latch.imm_data_in)
        
        # Decoder outputs
        connect(m, decoder.alu_flags, decode_latch.instr_flags_in)
        # connect(m, decoder.alu_flags, imm_builder.instr_flags)
        connect(m, decoder.reg_addr, decode_latch.reg_address_in)
        connect(m, decoder.functions, decode_latch.alu_func_in)
        
        # Decode latch outputs
        connect(m, decode_latch.instr_flags_out, execute_latch.instr_flags_in) 
        # connect(m, decode_latch.instr_flags_out, addr_builder.instr_flags) 
        connect(m, decode_latch.imm_data_out, execute_latch.imm_data_in)
        # connect(m, decode_latch.imm_data_out, addr_builder.imm_data) 
        connect(m, decode_latch.alu_func_out, execute_latch.alu_func_in)
        connect(m, decode_latch.reg_address_out, regbank.reg_addr)
        connect(m, decode_latch.pc_out, execute_latch.pc_in)
        # connect(m, decode_latch.pc_out, addr_builder.PC_in)
        
        # Execute latch outputs
        connect(m, execute_latch.alu_func_out , alu.functions)
        connect(m, execute_latch.pc_out , opbuilder.pc)
        connect(m, execute_latch.imm_data_out , opbuilder.imm)
        connect(m, execute_latch.reg_data_out , opbuilder.data_regbank)
        # connect(m, execute_latch.inst_flags_out , opbuilder.) ## ???
        connect(m, execute_latch.inst_flags_out, alu.flags_in)
        
        # Op Builder outputs
        connect(m, opbuilder.alu_buses, alu.data_buses)
        
        # ALU outputs
        connect(m, alu.rd_bus, regbank.rd_bus)
        
        # regbank outputs
        connect(m, regbank.rs_buses, execute_latch.reg_data_in)
        # connect(m, regbank.rs_buses, addr_builder.rs_data)
        
        return m