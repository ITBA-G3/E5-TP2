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
    enable : In(1)

    def elaborate(self, platform):
        m = Module()

        program = [
            0b0000000_00000_00001_000_00000_0000000,    # nop
            0x3e800093,    # addi x1, x0, 1000
            0x3e900093,    # addi x1, x0, 1001
            0x3ea00093,    # addi x1, x0, 1002
            0x3e800093,    # addi x1, x0, 1000
            0x3e900093,    # addi x1, x0, 1001
            0x3ea00093,    # addi x1, x0, 1002
            # -------------------------------
            0xfe208ee3,    # beq  x1, x2, -4
            0x3e800093,    # addi x1, x0, 1000
            0x3e900093,    # addi x1, x0, 1001
            0x3ea00093,    # addi x1, x0, 1002
            0xfe101de3,     # bne x0, x1, -6
            0x3ea00093,    # addi x1, x0, 1002
            0x3e900093,    # addi x1, x0, 1001
            0x3e800093    # addi x1, x0, 1000
        ]

        # 256-word 32-bit wide instr mem
        mem = Memory(width=32, depth=256, init=program +
        [0b0000000_00000_00001_000_00000_0000000]*(256-len(program)),
        attrs={"ram_style": "block"}) # NOP pad the rest


        rdport = mem.read_port()
        m.submodules.rdport = rdport

        with m.If(~self.resetn & self.enable):
            m.d.comb += [
                self.pc.pc.eq(self.pc_update.pc),        
                self.instr.instr.eq(rdport.data)
            ]
        
        with m.Elif(~self.enable):
            m.d.comb += [ self.pc.pc.eq(self.pc.pc)]

        m.d.comb += rdport.addr.eq(self.pc.pc)

        return m
