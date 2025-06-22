import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))


from amaranth import *
from bus_signatures import branch_flags, imm_data, fetch_operand_b, decode_alu_fun, decode_alu_flags, decode_reg_addr, fetch_decode, fetch_operand_b
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

class Decode_latch(wiring.Component):

    instr_flags_in : In(decode_alu_flags())
    reg_address_in : In(decode_reg_addr())
    alu_func_in : In(decode_alu_fun())
    pc_in : In(fetch_operand_b())
    imm_data_in : In(imm_data())
    branch_flags_in : In(branch_flags())
    decode_enable : In(1)
    decode_mux : In(1)

    instr_flags_out : Out(decode_alu_flags())
    reg_address_out : Out(decode_reg_addr())
    alu_func_out : Out(decode_alu_fun())
    pc_out : Out(fetch_operand_b())
    imm_data_out : Out(imm_data())
    branch_flags_out : Out(branch_flags())

    def elaborate(self, platform):
        
        obj_decode_reg_addr = decode_reg_addr()
        obj_decode_alu_flags = decode_alu_flags()
        obj_decode_alu_fun = decode_alu_fun()
        obj_fetch_operand_b = fetch_operand_b()
        obj_imm_data = imm_data()
        obj_branch_flags = branch_flags()
        
        m = Module()
        with m.If(self.decode_mux):
            for (path, flow, value) in list(decode_alu_flags.flatten(obj_decode_alu_flags, self.instr_flags_in)):
                dst = self.instr_flags_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(0)
            
            for (path, flow, value) in list(decode_reg_addr.flatten(obj_decode_reg_addr, self.reg_address_in)):
                dst = self.reg_address_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(0)
            
            for (path, flow, value) in list(decode_alu_fun.flatten(obj_decode_alu_fun, self.alu_func_in)):
                dst = self.alu_func_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(0)
            
            for (path, flow, value) in list(fetch_operand_b.flatten(obj_fetch_operand_b, self.pc_in)):
                dst = self.pc_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(0)
            
            for (path, flow, value) in list(imm_data.flatten(obj_imm_data, self.imm_data_in)):
                dst = self.imm_data_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(0)
            
            for (path, flow, value) in list(branch_flags.flatten(obj_branch_flags, self.branch_flags_in)):
                dst = self.branch_flags_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(0)

        with m.Elif(self.decode_enable):                    # :+1:
            for (path, flow, value) in list(decode_alu_flags.flatten(obj_decode_alu_flags, self.instr_flags_in)):
                dst = self.instr_flags_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(value)
            
            for (path, flow, value) in list(decode_reg_addr.flatten(obj_decode_reg_addr, self.reg_address_in)):
                dst = self.reg_address_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(value)
            
            for (path, flow, value) in list(decode_alu_fun.flatten(obj_decode_alu_fun, self.alu_func_in)):
                dst = self.alu_func_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(value)
            
            for (path, flow, value) in list(fetch_operand_b.flatten(obj_fetch_operand_b, self.pc_in)):
                dst = self.pc_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(value)
            
            for (path, flow, value) in list(imm_data.flatten(obj_imm_data, self.imm_data_in)):
                dst = self.imm_data_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(value)

            for (path, flow, value) in list(branch_flags.flatten(obj_branch_flags, self.branch_flags_in)):
                dst = self.branch_flags_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.sync += dst.eq(value)

        return m