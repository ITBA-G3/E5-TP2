from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth_boards import arty_a7
from signatures_test import alu_regbank

class ALU(wiring.Component):
    # alu_buses.rs1_data: In(32)
    # alu_buses.rs2_data: In(32)
    # alu_buses.rd_data: Out(32)

    alu_buses: In(alu_regbank())

    func3: In(3)
    func7: In(7)
    shamt: In(5)

    isALUreg: In(1)
    isALUimm: In(1)
    isBranch: In(1)
    isJALR: In(1)
    isJAL: In(1)
    isAUIPC: In(1)
    isLUI: In(1)
    isLoad: In(1)
    isStore: In(1)

    EQ: Out(1)
    EQM: Out(1)
    EQM_U: Out(1)

    def __init__(self):
        super().__init__()

    def elaborate(self, platform):
        m = Module()
        m.domains.sync = ClockDomain("sync")
        m.d.comb += self.alu_buses.rd_data.eq(0)

        with m.If(self.isALUreg | self.isALUimm):
            with m.Switch(self.func3):
                with m.Case(0b000):
                    with m.If((self.func7[5]) & self.isALUreg):
                        m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs1_data - self.alu_buses.rs2_data)
                    with m.Else():
                        m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs1_data + self.alu_buses.rs2_data)
                with m.Case(0b111):
                    m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs1_data & self.alu_buses.rs2_data)
                with m.Case(0b110):
                    m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs1_data | self.alu_buses.rs2_data)
                with m.Case(0b100):
                    m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs1_data ^ self.alu_buses.rs2_data)
                with m.Case(0b001):
                    m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs1_data << self.shamt)
                with m.Case(0b101):
                    with m.If(self.func7[5]):
                        m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs1_data.as_signed() >> self.shamt)
                    with m.Else():
                        m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs1_data >> self.shamt)
                with m.Case(0b010):
                    m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs1_data.as_signed() < self.alu_buses.rs2_data.as_signed())
                with m.Case(0b011):
                    m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs1_data < self.alu_buses.rs2_data)

        with m.Elif(self.isAUIPC):
            m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs1_data + self.alu_buses.rs2_data)

        with m.Elif(self.isLUI):
            m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs2_data)

        with m.Elif(self.isJAL | self.isJALR):
            m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs1_data + 4)

        with m.Elif(self.isLoad | self.isStore):
            m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs1_data + self.alu_buses.rs2_data)

        return m
