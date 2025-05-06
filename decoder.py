from amaranth import *
from signatures_test import decode_alu_flags, decode_reg_addr, decode_alu_fun, decode_imm
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

class Decoder(wiring.Component):
    
    instr: In(32)     # 32-bit instruction
    
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

    # Iimm = Signal(32)
    # Uimm = Signal(32)
    # Simm = Signal(32)
    # Bimm = Signal(32)
    # Jimm = Signal(32)
    imm_data: Out(decode_imm())
    
    # Creo que todas estas declaraciones se tienen que hacer porque estoy simulando y quiero acceder 
    # a estas señales desde el tb entonces tienen que ser parte de la clase "Decoder". No se si
    # cuando hagamos el wiring tienen que estar estas señales en el constructor o no.
    
    def elaborate(self, platform):
        m = Module()
        
        m.domains.sync = ClockDomain("sync")

        # Decode instruction from opcode bits ([0:7] 6 bits menos significativos)
        opcode = self.instr[0:7]
        
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
            self.reg_addr.rs1_addr.eq(self.instr[15:20]),
            self.reg_addr.rs2_addr.eq(self.instr[20:25]),
            self.reg_addr.rd_addr.eq(self.instr[7:12]),

            self.functions.func3.eq(self.instr[12:15]),
            self.functions.func7.eq(self.instr[25:32]),
        ]

        # Immediate values (sign-extended)
        m.d.comb += [
            self.imm_data.Iimm.eq(Cat(self.instr[20:32], self.instr[31].replicate(20))),
            self.imm_data.Simm.eq(Cat(self.instr[7:12], self.instr[25:32], self.instr[31].replicate(20))),
            self.imm_data.Bimm.eq(Cat(C(0, 1), self.instr[8:12], self.instr[25:31], self.instr[7], self.instr[31].replicate(19))),
            self.imm_data.Uimm.eq(Cat(C(0, 12), self.instr[12:32])),
            self.imm_data.Jimm.eq(Cat(C(0, 1), self.instr[21:31], self.instr[20], self.instr[12:20], self.instr[31].replicate(11))),
        ]
        
        return m