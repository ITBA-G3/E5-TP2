from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from bus_signatures import fetch_operand_b, operand_b_alu, operand_b_regbank, decode_imm, operand_b_mux
from amaranth_boards import arty_a7

class opBuilder(wiring.Component):
    
    data_regbank : In(operand_b_regbank())
    imm : In(decode_imm())
    pc : In(fetch_operand_b())
    alu_buses : Out(operand_b_alu())
    muxes: In(operand_b_mux())
    
            
    def elaborate(self, platform):
        m = Module()
        
        with m.If(~self.muxes.muxA):     # A = rs1_data  
            m.d.comb += self.alu_buses.A.eq(self.data_regbank.rs1_data)
        with m.Else():                  # A = PC
            m.d.comb += self.alu_buses.A.eq(self.pc.pc)    
        
        with m.Switch(self.muxes.muxB):
            with m.Case(0b000):         # B = rs2_data
                m.d.comb += self.alu_buses.B.eq(self.data_regbank.rs2_data)
            with m.Case(0b001):         # B = Iimm
                m.d.comb += self.alu_buses.B.eq(self.imm.Iimm)
            with m.Case(0b010):         # B = Uimm
                m.d.comb += self.alu_buses.B.eq(self.imm.Uimm)
            with m.Case(0b011):         # B = Simm
                m.d.comb += self.alu_buses.B.eq(self.imm.Simm)
            with m.Case(0b100):         # B = Bimm
                m.d.comb += self.alu_buses.B.eq(self.imm.Bimm)
            with m.Case(0b101):         # B = Jimm
                m.d.comb += self.alu_buses.B.eq(self.imm.Jimm)
        # :)
        
        return m