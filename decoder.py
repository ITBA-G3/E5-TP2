from amaranth import *
from bus_signatures import branch_flags, decode_alu_flags, decode_reg_addr, decode_alu_fun, fetch_decode
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
# from amaranth_boards.de0_cv import DE0CVPlatform

class Decoder(wiring.Component):
    
    instr: In(fetch_decode())     # 32-bit instruction
    

    alu_flags: Out(decode_alu_flags())
    branch_flags : Out(branch_flags())

    isSystem = Signal()


    reg_addr: Out(decode_reg_addr())


    functions: Out(decode_alu_fun())

    RS1_ADDR = Signal(5)
    RS2_ADDR = Signal(5)

    def elaborate(self, platform):
        m = Module()
        
        m.domains.sync = ClockDomain("sync")

        # Decode instruction from opcode bits ([0:7] 6 bits menos significativos)
        opcode = self.instr.instr[0:7]
        branch = self.instr.instr[12:15]
        
        m.d.comb += [
            self.alu_flags.isALUreg.eq(opcode == 0b0110011),         
            self.alu_flags.isALUimm.eq(opcode == 0b0010011),
            self.alu_flags.isBranch.eq(opcode == 0b1100011),
            self.alu_flags.isJALR.eq(opcode == 0b1100111),
            self.alu_flags.isJAL.eq(opcode == 0b1101111),
            self.alu_flags.isAUIPC.eq(opcode == 0b0010111),
            self.alu_flags.isLUI.eq(opcode == 0b0110111),
            self.alu_flags.isLoad.eq(opcode == 0b0000011),
            self.alu_flags.isStore.eq(opcode == 0b0100011),
            self.isSystem.eq(opcode == 0b1110011),
        ]
        with m.If(opcode == 0b1100011):
            with m.Switch(branch):
                with m.Case(0b000):
                    m.d.comb += [
                        self.branch_flags.beq.eq(1),
                        self.branch_flags.bne.eq(0),
                        self.branch_flags.blt.eq(0),
                        self.branch_flags.bge.eq(0),
                        self.branch_flags.bltu.eq(0),
                        self.branch_flags.bgeu.eq(0)]
                with m.Case(0b001):
                    m.d.comb += [
                        self.branch_flags.beq.eq(0),
                        self.branch_flags.bne.eq(1),
                        self.branch_flags.blt.eq(0),
                        self.branch_flags.bge.eq(0),
                        self.branch_flags.bltu.eq(0),
                        self.branch_flags.bgeu.eq(0)]
                with m.Case(0b100):
                    m.d.comb += [
                        self.branch_flags.beq.eq(0),
                        self.branch_flags.bne.eq(0),
                        self.branch_flags.blt.eq(1),
                        self.branch_flags.bge.eq(0),
                        self.branch_flags.bltu.eq(0),
                        self.branch_flags.bgeu.eq(0)]
                with m.Case(0b101):
                    m.d.comb += [
                        self.branch_flags.beq.eq(0),
                        self.branch_flags.bne.eq(0),
                        self.branch_flags.blt.eq(0),
                        self.branch_flags.bge.eq(1),
                        self.branch_flags.bltu.eq(0),
                        self.branch_flags.bgeu.eq(0)]
                with m.Case(0b110):
                    m.d.comb += [
                        self.branch_flags.beq.eq(0),
                        self.branch_flags.bne.eq(0),
                        self.branch_flags.blt.eq(0),
                        self.branch_flags.bge.eq(0),
                        self.branch_flags.bltu.eq(1),
                        self.branch_flags.bgeu.eq(0)]
                with m.Case(0b111):
                    m.d.comb += [
                        self.branch_flags.beq.eq(0),
                        self.branch_flags.bne.eq(0),
                        self.branch_flags.blt.eq(0),
                        self.branch_flags.bge.eq(0),
                        self.branch_flags.bltu.eq(0),
                        self.branch_flags.bgeu.eq(1)]
                with m.Default():
                    m.d.comb += [
                        self.branch_flags.beq.eq(0),
                        self.branch_flags.bne.eq(0),
                        self.branch_flags.blt.eq(0),
                        self.branch_flags.bge.eq(0),
                        self.branch_flags.bltu.eq(0),
                        self.branch_flags.bgeu.eq(0)]
            
        with m.Else():
            m.d.comb += [
                self.branch_flags.beq.eq(0),
                self.branch_flags.bne.eq(0),
                self.branch_flags.blt.eq(0),
                self.branch_flags.bge.eq(0),
                self.branch_flags.bltu.eq(0),
                self.branch_flags.bgeu.eq(0)
            ]
        
        # Register fields
        m.d.comb += [
            self.reg_addr.rs1_addr.eq(self.instr.instr[15:20]),
            self.reg_addr.rs2_addr.eq(self.instr.instr[20:25]),
            self.reg_addr.rd_addr.eq(self.instr.instr[7:12]),

            self.functions.func3.eq(self.instr.instr[12:15]),
            self.functions.func7.eq(self.instr.instr[25:32])
        ]
        m.d.comb += self.RS1_ADDR.eq(self.instr.instr[15:20])
        m.d.comb += self.RS2_ADDR.eq(self.instr.instr[20:25])
        
        return m
    
# if __name__ == "__main__":
#     platform = DE0CVPlatform()

#     core = Decoder()
#     platform.build(core, do_build=True, do_program=False)

    
