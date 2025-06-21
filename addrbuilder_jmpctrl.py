from amaranth import *
from bus_signatures import decode_alu_flags, operand_b_regbank, alu_regbank, imm_data, addrbuilder_enable, fetch_operand_b, pc_update
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

class addrbuilder(wiring.Component):
    
    PC_out: Out(pc_update())
    
    PC_in: In(fetch_operand_b())        # ESTE ES EL PC QUE SALE DEL FETCH Y VA AL OP BUILDER
    
    instr_flags: In(decode_alu_flags())

    imm_data: In(imm_data())


    alu_out: In(alu_regbank())          # ALU output data: not sure if i need it
    
    rs_data: In(operand_b_regbank())    # rs_1 y rs_2 data: needed to build the address


    # addrbuilder_enable: In(1)  # Enable signal for the addrbuilder TODO: Control Signal

    isSystem = Signal()

    def elaborate(self, platform):
        m = Module()
        
        m.domains.sync = ClockDomain("sync")

        # with m.If(self.addrbuilder_enable): # TODO: Control Signal

        with m.If(self.instr_flags.isALUreg | self.instr_flags.isALUimm | self.instr_flags.isLUI | self.instr_flags.isAUIPC):
            m.d.comb += [
                self.PC_out.pc.eq(self.PC_in.pc + 1)  # For these instr PC needs no special treatment    
            ]

        # INSTRUCCIONES DE SALTOS QUE MODIFICAN EL PC

        with m.If(self.instr_flags.isBranch):       # Politica de siempre tomar el salto.
            m.d.comb += [
                self.PC_out.pc.eq(self.PC_in.pc + self.imm_data.imm)        # TODO: Por ahora estoy tomando todos los branches...
            ]
        with m.If(self.instr_flags.isJAL):
            m.d.comb += [
                self.PC_out.pc.eq(self.PC_in.pc + self.imm_data.imm)
            ]
        with m.If(self.instr_flags.isJALR):
            m.d.comb += [
                self.PC_out.pc.eq((self.PC_in.pc + self.rs_data.rs1_data + self.imm_data.imm) & 0xFFFFFFFE)           # rs1 + imm asegurando que el bit menos significativo es cero
            ]

        return m