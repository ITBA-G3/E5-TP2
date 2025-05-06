from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth_boards import arty_a7

class RegBank (wiring.Component):

    rs1_data: Out(32)
    rs2_data: Out(32)
    rd_data: In(32)

    rs1_addr: In(5)
    rs2_addr: In(5)
    rd_addr: In(5)

    we: In(1)

    def elaborate (self, platform):
        m = Module()

        regBank = Array([Signal(32) for x in range(32)],)

        # the reading process is combinational, so we can use the combinational domain
        m.d.comb += [
            self.rs1_data.eq(regBank[self.rs1_addr]),
            self.rs2_data.eq(regBank[self.rs2_addr]),
        ]

        # the writing process is clk-syncronous, so we can use the sync domain
        with m.If((self.we) & (self.rd_addr != 0)):
            m.d.sync += [
                regBank[self.rd_addr].eq(self.rd_data),
            ]

        return m

