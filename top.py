from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out, connect
from amaranth_boards import arty_a7

from regbank import RegBank
from alu import ALU
from decoder import Decoder
from fetch import Fetch
from opbuilder import opBuilder
from immbuilder import Immbuilder
from addrbuilder_jmpctrl import Addrbuilder
from Amaranth.Modules.Latches.decode_latch import Decode_latch
from Amaranth.Modules.Latches.execute_latch import Execute_latch
from Amaranth.Modules.Latches.retire_latch import Retire_latch
from Amaranth.Modules.Pipeline_Controller.pipeline import Pipeline

class Top (Elaboratable):
    def __init__(self):
        super().__init__()

    def elaborate(self, platform):
        m = Module()

        m.submodules.regbank = regbank = RegBank()
        m.submodules.decode_latch = decode_latch = Decode_latch()
        m.submodules.execute_latch = execute_latch = Execute_latch()
        m.submodules.retire_latch = retire_latch = Retire_latch()
        m.submodules.alu = alu = ALU()
        m.submodules.decoder = decoder = Decoder()
        m.submodules.fetch = fetch = Fetch()
        m.submodules.opbuilder = opbuilder = opBuilder()
        m.submodules.imm_builder = imm_builder = Immbuilder()
        m.submodules.addr_builder = addr_builder = Addrbuilder()
        m.submodules.pipeline = pipeline = Pipeline()
        
        
        self.decode_latch = decode_latch
        self.execute_latch = execute_latch
        self.retire_latch = retire_latch
        self.alu = alu
        self.regbank = regbank
        self.decoder = decoder
        self.fetch = fetch
        self.opbuilder = opbuilder
        self.imm_builder = imm_builder
        self.addr_builder = addr_builder
        self.pipeline = pipeline

        # Fetch inputs
        connect(m, fetch.pc_update, addr_builder.PC_out)

        # Fetch outputs
        connect(m, fetch.pc, decode_latch.pc_in)
        connect(m, fetch.instr, decoder.instr)
        connect(m, fetch.instr, imm_builder.instr)
        
        # Imm builder outputs
        connect(m, imm_builder.imm_data, decode_latch.imm_data_in)
        
        # Decoder outputs
        connect(m, decoder.alu_flags, decode_latch.instr_flags_in)
        connect(m, decoder.alu_flags, imm_builder.instr_flags)
        connect(m, decoder.alu_flags, pipeline.instr_flags_fetch)
        connect(m, decoder.reg_addr, decode_latch.reg_address_in)
        connect(m, decoder.reg_addr, pipeline.reg_addr_fetch)
        connect(m, decoder.functions, decode_latch.alu_func_in)
        connect(m, decoder.branch_flags, decode_latch.branch_flags_in)
        
        # Decode latch outputs
        connect(m, decode_latch.instr_flags_out, execute_latch.instr_flags_in) 
        connect(m, decode_latch.instr_flags_out, addr_builder.instr_flags) 
        connect(m, decode_latch.instr_flags_out, pipeline.instr_flags_decode)
        connect(m, decode_latch.imm_data_out, execute_latch.imm_data_in)
        connect(m, decode_latch.imm_data_out, addr_builder.imm_data) 
        connect(m, decode_latch.alu_func_out, execute_latch.alu_func_in)
        connect(m, decode_latch.reg_address_out.rs1_addr, regbank.reg_addr.rs1_addr)
        connect(m, decode_latch.reg_address_out.rs2_addr, regbank.reg_addr.rs2_addr)
        connect(m, decode_latch.reg_address_out, pipeline.reg_addr_decode)
        connect(m, decode_latch.pc_out, execute_latch.pc_in)
        connect(m, decode_latch.pc_out, addr_builder.PC_in)
        connect(m, decode_latch.branch_flags_out, execute_latch.branch_flags_in)
        connect(m, decode_latch.reg_address_out.rd_addr, execute_latch.rd_in)

        # regbank outputs
        connect(m, regbank.rs_buses, execute_latch.reg_data_in)
        connect(m, regbank.rs_buses, addr_builder.rs_data)
        
        # Execute latch outputs TODO: Falta el pipeline acá
        connect(m, execute_latch.alu_func_out , alu.functions)
        connect(m, execute_latch.pc_out , opbuilder.pc)
        connect(m, execute_latch.imm_data_out , opbuilder.imm)
        connect(m, execute_latch.reg_data_out , opbuilder.data_regbank)
        connect(m, execute_latch.instr_flags_out , opbuilder.instr_flags)
        connect(m, execute_latch.instr_flags_out, alu.flags_in)
        connect(m, execute_latch.instr_flags_out, pipeline.instr_flags_execute)
        connect(m, execute_latch.rd_out, pipeline.rd_execute)
        connect(m, execute_latch.branch_flags_out, pipeline.branch_flags_execute)
        connect(m, execute_latch.rd_out, retire_latch.rd_in)
        connect(m, execute_latch.instr_flags_out, retire_latch.instr_flags_in)
        
        # Op Builder outputs
        connect(m, opbuilder.alu_buses, alu.data_buses)
        
        # ALU outputs
        connect(m, alu.rd_bus, retire_latch.rd_data_in)

        # Retire_Latch outputs
        connect(m, retire_latch.rd_data_out, regbank.rd_bus)
        connect(m, retire_latch.rd_out, regbank.reg_addr.rd_addr)
        connect(m, retire_latch.rd_out, pipeline.rd_retire)
        connect(m, retire_latch.instr_flags_out, regbank.instr_flags)
        connect(m, retire_latch.instr_flags_out, pipeline.instr_flags_retire)

        # Conexión de señales de control de latches
        connect(m, pipeline.decode_enable, decode_latch.decode_enable)
        connect(m, pipeline.decode_mux, decode_latch.decode_mux)
        connect(m, pipeline.execute_enable, execute_latch.enable)
        connect(m, pipeline.execute_mux, execute_latch.mux)
        connect(m, pipeline.retire_enable, retire_latch.enable)
        connect(m, pipeline.retire_mux, retire_latch.mux)
        connect(m, pipeline.addr_builder_enable, addr_builder.addrbuilder_enable)
        connect(m, pipeline.addr_builder_mux, addr_builder.mux)
        connect(m, pipeline.fetch_enable, fetch.resetn)

        # connect(m, regbank.rs_buses, addr_builder.rs_data)
        
        return m