from amaranth import *
from bus_signatures import decode_alu_flags, imm_data, fetch_decode
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

class Immbuilder(wiring.Component):
    
    instr: In(fetch_decode())     # 32-bit instruction

    instr_flags: In(decode_alu_flags())

    isSystem = Signal()

    imm_data: Out(imm_data())
    
    
    def elaborate(self, platform):
        m = Module()
        
        m.domains.sync = ClockDomain("sync")


        with m.If(self.instr_flags.isALUimm | self.instr_flags.isJALR | self.instr_flags.isLoad):  # Iimm          # ALU with immediates, JALR, Load --> imm
            m.d.comb += [
                self.imm_data.imm.eq(Cat(self.instr.instr[20:32], self.instr.instr[31].replicate(20))),
            ]
            
        with m.If(self.instr_flags.isStore):              # Store instructions --> Simm
            m.d.comb += self.imm_data.imm.eq(Cat(self.instr.instr[7:12], self.instr.instr[25:32], self.instr.instr[31].replicate(20))),    
            
        with m.If(self.instr_flags.isBranch):             # Conditional Branch instructions --> Bimm
            m.d.comb += self.imm_data.imm.eq(Cat(C(0, 1), self.instr.instr[8:12], self.instr.instr[25:31], self.instr.instr[7], self.instr.instr[31].replicate(19))),
            
        with m.If(self.instr_flags.isLUI | self.instr_flags.isAUIPC):   # LUI, AUIPC instructions --> Uimm
            m.d.comb += self.imm_data.imm.eq(Cat(C(0, 12), self.instr.instr[12:32])),

        with m.If(self.instr_flags.isJAL):                # Unconditional jumps JAL instruction --> Jimm
            m.d.comb += self.imm_data.imm.eq(Cat(C(0, 1), self.instr.instr[21:31], self.instr.instr[20], self.instr.instr[12:20], self.instr.instr[31].replicate(11))),
        
        
        
        return m