from amaranth import *
#from amaranth_boards import arty_a7

class ALU(Elaboratable):
    def __init__(self):
        self.A = Signal(32)
        self.B = Signal(32)
        self.func3 = Signal(3)
        self.func7 = Signal(7)
        self.shamt = Signal(5)

        self.isALUreg = Signal()
        self.isALUimm = Signal()
        self.isBranch = Signal()
        self.isJALR   = Signal()
        self.isJAL    = Signal()
        self.isAUIPC  = Signal()
        self.isLUI    = Signal()
        self.isLoad   = Signal()
        self.isStore  = Signal()

        self.Q = Signal(32)
        self.EQ = Signal()
        self.EQM = Signal()
        self.EQM_U = Signal()

    def elaborate(self, platform):
        m = Module()
        m.domains.sync = ClockDomain("sync")
        m.d.comb += self.Q.eq(0)

        with m.If(self.isALUreg | self.isALUimm):
            with m.Switch(self.func3):
                with m.Case(0b000):
                    with m.If((self.func7[5]) & self.isALUreg):
                        m.d.comb += self.Q.eq(self.A - self.B)
                    with m.Else():
                        m.d.comb += self.Q.eq(self.A + self.B)
                with m.Case(0b111):
                    m.d.comb += self.Q.eq(self.A & self.B)
                with m.Case(0b110):
                    m.d.comb += self.Q.eq(self.A | self.B)
                with m.Case(0b100):
                    m.d.comb += self.Q.eq(self.A ^ self.B)
                with m.Case(0b001):
                    m.d.comb += self.Q.eq(self.A << self.shamt)
                with m.Case(0b101):
                    with m.If(self.func7[5]):
                        m.d.comb += self.Q.eq(self.A.as_signed() >> self.shamt)
                    with m.Else():
                        m.d.comb += self.Q.eq(self.A >> self.shamt)
                with m.Case(0b010):
                    m.d.comb += self.Q.eq(self.A.as_signed() < self.B.as_signed())
                with m.Case(0b011):
                    m.d.comb += self.Q.eq(self.A < self.B)

        with m.Elif(self.isAUIPC):
            m.d.comb += self.Q.eq(self.A + self.B)

        with m.Elif(self.isLUI):
            m.d.comb += self.Q.eq(self.B)

        with m.Elif(self.isJAL | self.isJALR):
            m.d.comb += self.Q.eq(self.A + 4)

        with m.Elif(self.isLoad | self.isStore):
            m.d.comb += self.Q.eq(self.A + self.B)

        return m
