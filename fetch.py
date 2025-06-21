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

        # 256-word 32-bit wide instr mem
        mem = Memory(width=32, depth=256, init=[
            0b0000000_00000_00001_000_00001_1101111,    # jal x1, 0
            0b0000000_00000_00001_000_00000_0000000,    # nop
            0b000000000111_00001_000_00001_0010011,    # addi x1, x1, 1
            0b0000000_00000_00001_000_00001_0110011,    # add x1, x0, x0
        ] + [0]*(256-4)) # zero pad the rest


        rdport = mem.read_port()
        m.submodules.rdport = rdport

        with m.If(~self.resetn):
            m.d.sync += [
                self.instr.instr.eq(rdport.data),
                self.pc.pc.eq(self.pc_update.pc)        # CHECK
            ]

        m.d.comb += rdport.addr.eq(self.pc.pc)

        return m
