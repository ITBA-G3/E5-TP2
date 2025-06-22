from amaranth import *
from bus_signatures import fetch_decode, fetch_operand_b
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

class Pipeline(wiring.Component):

    instr_flags_fetch : In()
    rd_fetch : In()
    rs1_fetch : In()
    rs2_fetch : In()

    instr_flags_decode : In()
    rd_decode : In()
    rs1_decode : In()
    rs2_decode : In()

    instr_flags_execute : In()
    rd_execute : In()

    instr_flags_retire : In()
    rd_retire : In()

    fetch_enable : Out()
    fetch_mux : Out()

    decode_enable : Out()
    decode_mux : Out()
    
    execute_enable : Out()
    execute_mux : Out()
    
    retire_enable : Out()
    retire_mux : Out()


    def elaborate(self, platform):
        m = Module()
        
        pass