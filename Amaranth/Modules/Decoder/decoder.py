from amaranth import *

class Decoder(Elaboratable):
    def __init__(self):
        self.instr = Signal(32)     # 32-bit instruction
        
        self.isALUreg = Signal()    # Example control signal
        self.isALUimm = Signal()
        self.isBranch = Signal()
        self.isJALR   = Signal()
        self.isJAL    = Signal()
        self.isAUIPC  = Signal()
        self.isLUI    = Signal()
        self.isLoad   = Signal()
        self.isStore  = Signal()
        self.isSystem = Signal()

        self.rs1Id = Signal(5)
        self.rs2Id = Signal(5)
        self.rdId  = Signal(5)

        self.funct3 = Signal(3)
        self.funct7 = Signal(7)

        self.Iimm = Signal(32)
        self.Uimm = Signal(32)
        self.Simm = Signal(32)
        self.Bimm = Signal(32)
        self.Jimm = Signal(32)
        
        # Creo que todas estas declaraciones se tienen que hacer porque estoy simulando y quiero acceder 
        # a estas señales desde el tb entonces tienen que ser parte de la clase "Decoder". No se si
        # cuando hagamos el wiring tienen que estar estas señales en el constructor o no.
    
    def elaborate(self, platform):
        m = Module()
        
        m.domains.sync = ClockDomain("sync")

        # Decode instruction from opcode bits ([0:7] 6 bits menos significativos)
        opcode = self.instr[0:7]
        
        m.d.comb += [
            self.isALUreg.eq(opcode == 0b0110011),         
            self.isALUimm.eq(opcode == 0b0010011),
            self.isBranch.eq(opcode == 0b1100011),
            self.isJALR.eq(opcode == 0b1100111),
            self.isJAL.eq(opcode == 0b1101111),
            self.isAUIPC.eq(opcode == 0b0010111),
            self.isLUI.eq(opcode == 0b0110111),
            self.isLoad.eq(opcode == 0b0000011),
            self.isStore.eq(opcode == 0b0100011),
            self.isSystem.eq(opcode == 0b1110011),
        ]
        
        # Register fields
        m.d.comb += [
            self.rs1Id.eq(self.instr[15:20]),
            self.rs2Id.eq(self.instr[20:25]),
            self.rdId.eq(self.instr[7:12]),

            self.funct3.eq(self.instr[12:15]),
            self.funct7.eq(self.instr[25:32]),
        ]

        # Immediate values (sign-extended)
        m.d.comb += [
            self.Iimm.eq(Cat(self.instr[20:32], self.instr[31].replicate(20))),
            self.Simm.eq(Cat(self.instr[7:12], self.instr[25:32], self.instr[31].replicate(20))),
            self.Bimm.eq(Cat(C(0, 1), self.instr[8:12], self.instr[25:31], self.instr[7], self.instr[31].replicate(19))),
            self.Uimm.eq(Cat(C(0, 12), self.instr[12:32])),
            self.Jimm.eq(Cat(C(0, 1), self.instr[21:31], self.instr[20], self.instr[12:20], self.instr[31].replicate(11))),
        ]
        
        return m