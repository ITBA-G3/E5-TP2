from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth_boards import arty_a7
from bus_signatures import operand_b_regbank, decode_reg_addr, alu_regbank

class RegBank (wiring.Component):

    # rs1_data: Out(32)
    # rs2_data: Out(32)
    rs_buses: Out(operand_b_regbank())
    
    # rd_data: In(32)
    rd_bus: In(alu_regbank())

    # rs1_addr: In(5)
    # rs2_addr: In(5)
    # rd_addr: In(5)
    reg_addr: In(decode_reg_addr())

    we: In(1)
    
    def __init__(self):
        super().__init__()

    def elaborate (self, platform):
        m = Module()

        regBank = Array([Signal(32) for x in range(32)],)

        # the reading process is combinational, so we can use the combinational domain
        m.d.comb += [
            self.rs_buses.rs1_data.eq(regBank[self.reg_addr.rs1_addr]),
            self.rs_buses.rs2_data.eq(regBank[self.reg_addr.rs2_addr]),
        ]

        # the writing process is clk-syncronous, so we can use the sync domain
        with m.If((self.we) & (self.reg_addr.rd_addr != 0)):
            m.d.sync += [
                regBank[self.reg_addr.rd_addr].eq(self.rd_bus.rd_data),
            ]

        return m

