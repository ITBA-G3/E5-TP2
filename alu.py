from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth_boards import arty_a7
from bus_signatures import alu_regbank, operand_b_alu, decode_alu_flags, decode_alu_fun

class ALU(wiring.Component):
    # data_buses.A: In(32)
    # data_buses.B: In(32)
    data_buses: In(operand_b_alu())

    # rd_bus.rd_data: Out(32)
    rd_bus: Out(alu_regbank())

    # func3: In(3)
    # func7: In(7)
    functions: In(decode_alu_fun())
    shamt: In(5)

    flags_in: In(decode_alu_flags())

    z_flag: Out(1)
    n_flag: Out(1)
    

    def __init__(self):
        super().__init__()

    def elaborate(self, platform):
        m = Module()
        m.domains.sync = ClockDomain("sync")
        # m.d.comb += self.rd_bus.rd_data.eq(0)
        
        m.d.comb += self.z_flag.eq(self.rd_bus.rd_data == 0)
        m.d.comb += self.n_flag.eq(self.rd_bus.rd_data[31])

        with m.If(self.flags_in.isALUreg | self.flags_in.isALUimm):
            with m.Switch(self.functions.func3):
                with m.Case(0b000):
                    with m.If((self.functions.func7[5]) & self.flags_in.isALUreg):
                        m.d.comb += self.rd_bus.rd_data.eq(self.data_buses.A - self.data_buses.B)
                    with m.Else():
                        m.d.comb += self.rd_bus.rd_data.eq(self.data_buses.A + self.data_buses.B)
                with m.Case(0b111):
                    m.d.comb += self.rd_bus.rd_data.eq(self.data_buses.A & self.data_buses.B)
                with m.Case(0b110):
                    m.d.comb += self.rd_bus.rd_data.eq(self.data_buses.A | self.data_buses.B)
                with m.Case(0b100):
                    m.d.comb += self.rd_bus.rd_data.eq(self.data_buses.A ^ self.data_buses.B)
                with m.Case(0b001):
                    m.d.comb += self.rd_bus.rd_data.eq(self.data_buses.A << self.shamt)
                with m.Case(0b101):
                    with m.If(self.functions.func7[5]):
                        m.d.comb += self.rd_bus.rd_data.eq(self.data_buses.A.as_signed() >> self.shamt)
                    with m.Else():
                        m.d.comb += self.rd_bus.rd_data.eq(self.data_buses.A >> self.shamt)
                with m.Case(0b010):
                    m.d.comb += self.rd_bus.rd_data.eq(self.data_buses.A.as_signed() < self.data_buses.B.as_signed())
                with m.Case(0b011):
                    m.d.comb += self.rd_bus.rd_data.eq(self.data_buses.A < self.data_buses.B)

        with m.Elif(self.flags_in.isAUIPC):
            m.d.comb += self.rd_bus.rd_data.eq(self.data_buses.A + self.data_buses.B)

        with m.Elif(self.flags_in.isLUI):
            m.d.comb += self.rd_bus.rd_data.eq(self.data_buses.B)

        with m.Elif(self.flags_in.isJAL | self.flags_in.isJALR):
            m.d.comb += self.rd_bus.rd_data.eq(self.data_buses.A + 4)

        with m.Elif(self.flags_in.isLoad | self.flags_in.isStore):
            m.d.comb += self.rd_bus.rd_data.eq(self.data_buses.A + self.data_buses.B)
        with m.Elif(self.flags_in.isBranch):
            m.d.comb += self.rd_bus.rd_data.eq(self.data_buses.A - self.data_buses.B)
        return m