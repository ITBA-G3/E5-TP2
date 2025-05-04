from amaranth import *

class RegBank (Elaboratable):
    def __init__(self):
        self.bank = Signal(32)
        pass

    def elaborate (self, platform):
        rs1_data = Signal(32)
        rs2_data = Signal(32)
        rd_data = Signal(32)

        rs1_addr = Signal(5)
        rs2_addr = Signal(5)
        rd_addr = Signal(5)

        we = Signal(1)

        regBank = Array([Signal(32) for x in range(32)])

        # the reading process is combinational, so we can use the combinational domain
        m.d.comb += [
            rs1_data.eq(regBank[rs1_addr]),
            rs2_data.eq(regBank[rs2_addr]),
        ]

        # the writing process is clk-syncronous, so we can use the sync domain
        with m.If(we):
            m.d.sync += [
                regBank[rd_addr].eq(rd_data),
            ]

        m = Module()
