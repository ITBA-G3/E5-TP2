import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))


from amaranth import *
from bus_signatures import alu_regbank, operand_b_regbank, imm_data, fetch_operand_b, decode_alu_fun, decode_alu_flags, decode_reg_addr, fetch_decode, fetch_operand_b
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

class Execute_latch(wiring.Component):

    instr_flags_in : In(decode_alu_flags())
    alu_func_in : In(decode_alu_fun())
    pc_in : In(fetch_operand_b())
    imm_data_in : In(imm_data())
    reg_data_in : In(operand_b_regbank())
    rd_in : In(5) 
    enable : In(1)
    mux : In(1)

    instr_flags_out : Out(decode_alu_flags())
    alu_func_out : Out(decode_alu_fun())
    pc_out : Out(fetch_operand_b())
    imm_data_out : Out(imm_data())
    reg_data_out : Out(operand_b_regbank())
    rd_out : Out(5)

    def elaborate(self, platform):
        m = Module()

        obj_decode_alu_flags = decode_alu_flags()
        obj_decode_alu_fun = decode_alu_fun()
        obj_fetch_operand_b = fetch_operand_b()
        obj_imm_data = imm_data()
        obj_operand_b_regbank = operand_b_regbank()
        obj_alu_regbank = alu_regbank()
        
        with m.If(self.mux):
            for (path, flow, value) in list(decode_alu_flags.flatten(obj_decode_alu_flags, self.instr_flags_in)):
                dst = self.instr_flags_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(0)

            for (path, flow, value) in list(decode_alu_fun.flatten(obj_decode_alu_fun, self.alu_func_in)):
                dst = self.alu_func_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(0)
            
            for (path, flow, value) in list(imm_data.flatten(obj_imm_data, self.imm_data_in)):
                dst = self.imm_data_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(0)

            for (path, flow, value) in list(fetch_operand_b.flatten(obj_fetch_operand_b, self.pc_in)):
                dst = self.pc_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(0)

            for (path, flow, value) in list(operand_b_regbank.flatten(obj_operand_b_regbank, self.reg_data_in)):
                dst = self.reg_data_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(0)

            m.d.sync += self.rd_out.eq(0)

        with m.Elif(self.enable):
            for (path, flow, value) in list(decode_alu_flags.flatten(obj_decode_alu_flags, self.instr_flags_in)):
                dst = self.instr_flags_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(value)

            for (path, flow, value) in list(decode_alu_fun.flatten(obj_decode_alu_fun, self.alu_func_in)):
                dst = self.alu_func_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(value)
            
            for (path, flow, value) in list(imm_data.flatten(obj_imm_data, self.imm_data_in)):
                dst = self.imm_data_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(value)

            for (path, flow, value) in list(fetch_operand_b.flatten(obj_fetch_operand_b, self.pc_in)):
                dst = self.pc_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(value)

            for (path, flow, value) in list(operand_b_regbank.flatten(obj_operand_b_regbank, self.reg_data_in)):
                dst = self.reg_data_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(value)

            
            m.d.sync += self.rd_out.eq(self.rd_in)
        return m