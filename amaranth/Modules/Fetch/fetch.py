from amaranth import *
# remember to do platform imports here

class Fetch(Elaboratable):
    def __init__(self):
        # self.clk = ClockSignal()
        # i think i can use the sync domain's ClockSignal
        self.resetn = Signal()
        self.instr = Signal(32)
        self.pc = Signal(32)

    def elaborate(self, platform):
        m = Module()

        # 256-word 32-bit wide instr mem
        mem = Memory(width=32, depth=256, init=[
            0b0000000_00000_00000_000_00000_0110011,    # nop
            0b0000000_00000_00000_000_00001_0110011,    # add x1, x0, x0
            0b000000000001_00001_000_00001_0010011,    # addi x1, x1, 1
        ] + [0]*(256-3)) # zero pad the rest


        rdport = mem.read_port()
        m.submodules.rdport = rdport

        with m.If(~self.resetn):
            m.d.sync += [
                self.instr.eq(rdport.data),
                self.pc.eq(self.pc + 1)
            ]

        m.d.comb += rdport.addr.eq(self.pc)

        return m
