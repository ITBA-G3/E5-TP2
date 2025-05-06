from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth_boards import arty_a7
from signatures_test import alu_regbank, decode_alu_flags, decode_alu_fun

class ALU(wiring.Component):
    # alu_buses.rs1_data: In(32)
    # alu_buses.rs2_data: In(32)
    # alu_buses.rd_data: Out(32)

    alu_buses: In(alu_regbank())

    # func3: In(3)
    # func7: In(7)
    functions: In(decode_alu_fun())
    shamt: In(5)

    flags_in: In(decode_alu_flags())

    EQ: Out(1)
    EQM: Out(1)
    EQM_U: Out(1)

    def __init__(self):
        super().__init__()

    def elaborate(self, platform):
        m = Module()
        m.domains.sync = ClockDomain("sync")
        m.d.comb += self.alu_buses.rd_data.eq(0)

        with m.If(self.flags_in.isALUreg | self.flags_in.isALUimm):
            with m.Switch(self.functions.func3):
                with m.Case(0b000):
                    with m.If((self.functions.func7[5]) & self.flags_in.isALUreg):
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
                    with m.If(self.functions.func7[5]):
                        m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs1_data.as_signed() >> self.shamt)
                    with m.Else():
                        m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs1_data >> self.shamt)
                with m.Case(0b010):
                    m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs1_data.as_signed() < self.alu_buses.rs2_data.as_signed())
                with m.Case(0b011):
                    m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs1_data < self.alu_buses.rs2_data)

        with m.Elif(self.flags_in.isAUIPC):
            m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs1_data + self.alu_buses.rs2_data)

        with m.Elif(self.flags_in.isLUI):
            m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs2_data)

        with m.Elif(self.flags_in.isJAL | self.flags_in.isJALR):
            m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs1_data + 4)

        with m.Elif(self.flags_in.isLoad | self.flags_in.isStore):
            m.d.comb += self.alu_buses.rd_data.eq(self.alu_buses.rs1_data + self.alu_buses.rs2_data)

        return m
