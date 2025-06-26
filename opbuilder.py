from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from bus_signatures import decode_alu_flags, imm_data, fetch_operand_b, operand_b_alu, operand_b_regbank, operand_b_mux
from amaranth_boards import arty_a7

class opBuilder(wiring.Component):
    
    data_regbank : In(operand_b_regbank())
    imm : In(imm_data())
    pc : In(fetch_operand_b())
    alu_buses : Out(operand_b_alu())
    muxes: In(operand_b_mux())
    instr_flags : In(decode_alu_flags())
    
            
    def elaborate(self, platform):
        m = Module()  
        
        with m.If(self.instr_flags.isALUreg):
            m.d.comb += self.alu_buses.A.eq(self.data_regbank.rs1_data)
            m.d.comb += self.alu_buses.B.eq(self.data_regbank.rs2_data)
        with m.Elif(self.instr_flags.isAUIPC):
            m.d.comb += self.alu_buses.A.eq(self.pc.pc)
            m.d.comb += self.alu_buses.B.eq(self.imm.imm)
        with m.Elif(self.instr_flags.isALUimm):
            m.d.comb += self.alu_buses.A.eq(self.data_regbank.rs1_data)
            m.d.comb += self.alu_buses.B.eq(self.imm.imm)
        with m.Elif(self.instr_flags.isBranch):
            m.d.comb += self.alu_buses.A.eq(self.data_regbank.rs1_data)
            m.d.comb += self.alu_buses.B.eq(self.data_regbank.rs2_data)
        with m.Elif(self.instr_flags.isJALR):
            m.d.comb += self.alu_buses.A.eq(self.data_regbank.rs1_data)
            m.d.comb += self.alu_buses.B.eq(self.imm.imm + 1)
        with m.Elif(self.instr_flags.isJAL):
            m.d.comb += self.alu_buses.A.eq(self.pc.pc + 1)
            m.d.comb += self.alu_buses.B.eq(self.imm.imm)
        with m.Elif(self.instr_flags.isLUI):
            m.d.comb += self.alu_buses.A.eq(self.data_regbank.rs1_data)
            m.d.comb += self.alu_buses.B.eq(self.imm.imm)
        with m.Elif(self.instr_flags.isLoad):
            m.d.comb += self.alu_buses.A.eq(self.data_regbank.rs1_data)
            m.d.comb += self.alu_buses.B.eq(self.imm.imm)
        with m.Elif(self.instr_flags.isStore):
            m.d.comb += self.alu_buses.A.eq(self.data_regbank.rs1_data)
            m.d.comb += self.alu_buses.B.eq(self.imm.imm)
        with m.Else():
            m.d.comb += self.alu_buses.A.eq(self.data_regbank.rs1_data)
            m.d.comb += self.alu_buses.B.eq(self.data_regbank.rs2_data)
        
        return m