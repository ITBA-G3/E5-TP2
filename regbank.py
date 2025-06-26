from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth_boards import arty_a7
from bus_signatures import decode_alu_flags, operand_b_regbank, decode_reg_addr, alu_regbank

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
    instr_flags : In(decode_alu_flags())

    uart_reg : Out(32)

    we: In(1)
    
    def __init__(self):
        super().__init__()

    def elaborate (self, platform):
        m = Module()

        regBank = Array([Signal(32) for x in range(32)])

        # the reading process is combinational, so we can use the combinational domain
        m.d.comb += [
            self.rs_buses.rs1_data.eq(regBank[self.reg_addr.rs1_addr]),
            self.rs_buses.rs2_data.eq(regBank[self.reg_addr.rs2_addr])
        ]

        m.d.comb += self.uart_reg.eq(regBank[31])

        # the writing process is clk-syncronous, so we can use the sync domain
        with m.If((self.we) & (self.reg_addr.rd_addr != 0) & self.reg_addr.rd_addr <len(regBank)):
            for i in range(len(regBank)):
                with m.If(self.reg_addr.rd_addr == i):
                    m.d.comb += regBank[i].eq(self.rd_bus.rd_data)
                with m.Else():
                    m.d.comb += regBank[i].eq(regBank[i])

        with m.Else():
            for i in range(len(regBank)):
                m.d.comb += regBank[i].eq(regBank[i])
        #TODO: Hacer la conexión con la memoria

        return m

