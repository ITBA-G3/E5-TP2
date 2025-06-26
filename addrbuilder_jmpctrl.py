from amaranth import *
from bus_signatures import decode_alu_flags, operand_b_regbank, alu_regbank, imm_data, addrbuilder_enable, fetch_operand_b, pc_update
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

class Addrbuilder(wiring.Component):
    
    PC_out: Out(pc_update())
    
    PC_in: In(fetch_operand_b())        # ESTE ES EL PC QUE SALE DEL FETCH Y VA AL OP BUILDER
    
    instr_flags: In(decode_alu_flags())

    imm_data: In(imm_data())

    rs_data: In(operand_b_regbank())    # rs_1 y rs_2 data: needed to build the address

    saved_pc = Signal(32)

    addrbuilder_enable: In(1)  # Enable signal for the addrbuilder TODO: Control Signal
    mux : In(1)

    isSystem = Signal()
    
    # #########
    # fetch_enable: Out(1)  # Enable signal for the fetch stage
    # prev_enable = Signal()
    # #######

    def elaborate(self, platform):
        m = Module()
        
        # m.domains.sync = ClockDomain("sync")

        # INSTRUCCIONES DE SALTOS QUE MODIFICAN EL PC
        # with m.If((self.saved_pc == self.PC_out.pc) & self.saved_pc != 0):
        #     with m.If(self.addrbuilder_enable):
        #         m.d.comb += self.PC_out.pc.eq(self.saved_pc + 1)

        # with m.Else():

        with m.If(self.addrbuilder_enable): # TODO: Control Signal
                m.d.comb += self.PC_out.pc.eq(self.PC_in.pc + 1)  # Default case, increment PC by 1
        
        # with m.If(self.addrbuilder_enable): # TODO: Control Signal
        
        #     with m.If (~prev_enable):
        #         m.d.sync += self.PC_out.pc.eq(self.saved_pc)
        #     with m.Else:
        #         m.d.comb += self.PC_out.pc.eq(self.PC_in.pc + 1)  # Default case, increment PC by 1
            
        # m.d.comb += prev_enable.eq(self.addrbuilder_enable)  # Save the previous enable state
            # with m.If(self.PC_in.pc == 0xFFFFFFFF):
            #     m.d.comb += self.PC_out.pc.eq(self.saved_pc)
                
        with m.Elif(self.mux):
            m.d.comb += self.PC_out.pc.eq(self.saved_pc)
        
        with m.Elif(self.instr_flags.isBranch):       # Politica de siempre tomar el salto.
            m.d.comb += [
                self.PC_out.pc.eq(self.PC_in.pc + self.imm_data.imm),        # TODO: Por ahora estoy tomando todos los branches...
            ]
            m.d.sync += self.saved_pc.eq(self.PC_in.pc)
    
        with m.Elif(self.instr_flags.isJAL):
            m.d.comb += self.PC_out.pc.eq(self.PC_in.pc + self.imm_data.imm)
        
        with m.Elif(self.instr_flags.isJALR):
            m.d.comb += self.PC_out.pc.eq(self.rs_data.rs1_data + self.imm_data.imm) #& 0xFFFFFFFE)           # rs1 + imm asegurando que el bit menos significativo es cero
        
        with m.Else():
            m.d.comb += self.PC_out.pc.eq(self.PC_in.pc)
    
        # with m.If(~ self.addrbuilder_enable):
        #     m.d.comb += self.PC_out.pc.eq(self.PC_in.pc)

        return m