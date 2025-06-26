import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))


from amaranth import *
from bus_signatures import alu_regbank, operand_b_regbank, imm_data, fetch_operand_b, decode_alu_fun, decode_alu_flags, decode_reg_addr, fetch_decode, fetch_operand_b
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

class Retire_latch(wiring.Component):

    instr_flags_in : In(decode_alu_flags())
    rd_data_in : In(alu_regbank())
    rd_in : In(5) 
    enable : In(1)
    mux : In(1)

    instr_flags_out : Out(decode_alu_flags())
    rd_data_out : Out(alu_regbank())
    rd_out : Out(5)
    
    def elaborate(self, platform):
        m = Module()

        obj_decode_alu_flags = decode_alu_flags()
        obj_alu_regbank = alu_regbank()
        
        # with m.If(self.mux):
        #     for (path, flow, value) in list(decode_alu_flags.flatten(obj_decode_alu_flags, self.instr_flags_in)):
        #         dst = self.instr_flags_out
        #         for key in path:
        #             dst = getattr(dst, key)
        #         m.d.sync += dst.eq(0)

        #     for (path, flow, value) in list(alu_regbank.flatten(obj_alu_regbank, self.rd_data_in)):
        #         dst = self.rd_data_out
        #         for key in path:
        #             dst = getattr(dst, key)
        #         m.d.sync += dst.eq(0)
            
        #     m.d.sync += self.rd_out.eq(0)

        with m.If(self.enable):
            for (path, flow, value) in list(decode_alu_flags.flatten(obj_decode_alu_flags, self.instr_flags_in)):
                dst = self.instr_flags_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.comb += dst.eq(value)

            for (path, flow, value) in list(alu_regbank.flatten(obj_alu_regbank, self.rd_data_in)):
                dst = self.rd_data_out
                for key in path:
                    dst = getattr(dst, key)
                m.d.comb += dst.eq(value)

            m.d.comb += self.rd_out.eq(self.rd_in)
        
        return m