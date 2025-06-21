from amaranth import *
from bus_signatures import decode_alu_flags, decode_reg_addr, decode_alu_fun, fetch_decode
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth_boards.de0_cv import DE0CVPlatform

class Decoder(wiring.Component):
    
    instr: In(fetch_decode())     # 32-bit instruction
    
    # self.isALUreg = Signal()    # Example control signal
    # self.isALUimm = Signal()
    # self.isBranch = Signal()
    # self.isJALR   = Signal()
    # self.isJAL    = Signal()
    # self.isAUIPC  = Signal()
    # self.isLUI    = Signal()
    # self.isLoad   = Signal()
    # self.isStore  = Signal()
    alu_flags: Out(decode_alu_flags())

    isSystem = Signal()

    # self.rs1_addr = Signal(5)
    # self.rs2_addr = Signal(5)
    # self.rd_addr = Signal(5)
    reg_addr: Out(decode_reg_addr())

    # func3 = Signal(3)
    # func7 = Signal(7)
    functions: Out(decode_alu_fun())

    def elaborate(self, platform):
        m = Module()
        
        m.domains.sync = ClockDomain("sync")

        # Decode instruction from opcode bits ([0:7] 6 bits menos significativos)
        opcode = self.instr.instr[0:7]
        
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
        
        # Register fields
        m.d.comb += [
            self.reg_addr.rs1_addr.eq(self.instr.instr[15:20]),
            self.reg_addr.rs2_addr.eq(self.instr.instr[20:25]),
            self.reg_addr.rd_addr.eq(self.instr.instr[7:12]),

            self.functions.func3.eq(self.instr.instr[12:15]),
            self.functions.func7.eq(self.instr.instr[25:32]),
        ]
        
        return m
    
if __name__ == "__main__":
    platform = DE0CVPlatform()

    core = Decoder()
    platform.build(core, do_build=True, do_program=False)

    
