from amaranth import *
from bus_signatures import fetch_decode, fetch_operand_b, pc_update
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
# remember to do platform imports here 

class Fetch(wiring.Component):
        # self.clk = ClockSignal()
        # i think i can use the sync domain's ClockSignal
   
    instr : Out(fetch_decode())
    pc : Out(fetch_operand_b()) 
    resetn : In(1)
    pc_update : In(pc_update())

    def elaborate(self, platform):
        m = Module()

        program = [
            0b0000000_00000_00001_000_00000_0000000,    # nop
            0x3e800093,    # addi x1, x0, 1000
            0x3e800093,    # addi x1, x0, 1000
            # 0x3e800093,    # addi x1, x0, 1000
            # 0x7d008113,    # addi x2, x1, 2000
            # 0xc1810113,    # addi x2, x2, -1000
            0xfe208ee3,    # beq  x1, x2, -4
            # 0x00208263,       # beq  x1, x2, 4
            0xfe101fe3     # bne x0, x1, -2
            # 0x00518113,    # addi x2, x3, 5

        ]

        # 256-word 32-bit wide instr mem
        mem = Memory(width=32, depth=256, init=program +
        [0b0000000_00000_00001_000_00000_0000000]*(256-len(program)),
        attrs={"ram_style": "block"}) # NOP pad the rest


        rdport = mem.read_port()
        m.submodules.rdport = rdport

        with m.If(~self.resetn):
            m.d.comb += [           # ANTES ERA SYNC
                self.pc.pc.eq(self.pc_update.pc),        
                self.instr.instr.eq(rdport.data)
            ]

        m.d.comb += rdport.addr.eq(self.pc.pc)

        return m
