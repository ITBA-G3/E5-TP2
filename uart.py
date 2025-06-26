from amaranth import *
from amaranth.build import Platform
from amaranth.lib import wiring
from amaranth_boards.arty_a7 import ArtyA7_100Platform
from amaranth.lib.wiring import In, Out
from bus_signatures import data_uart, tx_uart, start_uart, ready_uart


class UART32(wiring.Component):
    # inputs
    data : In(data_uart())
    start : In(start_uart())
    
    tx : Out(tx_uart())
    ready : Out(ready_uart())

    def __init__(self):
        super().__init__()

    def elaborate(self, platform):
        m = Module()
#       8-n-1 frame
#       |– start –| b0 | b1 | b2 | b3 | b4 | b5 | b6 | b7 |– stop –|
        
        uart_pins = platform.request("uart", 0)
        m.d.comb += uart_pins.tx.o.eq(self.tx.tx)

        clk_freq = 100e6
        baud_rate = 115200

        # baud tick generator
        bit_period = int(clk_freq // baud_rate)
        baud_cnt = Signal(range(bit_period))
        baud_tick = Signal()
        print(f"UART TX: baud_divisor={bit_period}")
        
        with m.If(baud_cnt == bit_period - 1):
            m.d.sync += [
                baud_cnt.eq(0),
                baud_tick.eq(1)
            ]
        with m.Else():
            m.d.sync += [
                baud_cnt.eq(baud_cnt + 1),
                baud_tick.eq(0)
            ]
        
        # frame shift register
        trama = Signal(40)
        bit_cnt = Signal(range(40))
        sending = Signal(reset=0)
        m.d.comb += self.ready.ready.eq(~sending)

        # idle vs sending
        with m.If((self.start.start & self.ready.ready)):
            first_byte = self.data.data[0:8]
            m.d.sync += [
                trama.eq(Cat(
                            Const(0, 1), self.data.data[24:32], Const(1, 1),
                            Const(0, 1), self.data.data[16:24], Const(1, 1),
                            Const(0, 1), self.data.data[8:16], Const(1, 1),
                            Const(0, 1), self.data.data[0:8], Const(1, 1)
                            )),
                bit_cnt.eq(40),
                sending.eq(1)
            ]

        # shift a bit out on baud tick
        with m.If(baud_tick & sending):
            # m.d.sync += uart_pins.tx.o.eq(frame_reg[0])
            m.d.sync += [
                self.tx.tx.eq(trama[0]),
                bit_cnt.eq(bit_cnt - 1),
            ]

            with m.If(bit_cnt != 0):
                m.d.sync += [
                    trama.eq(trama >> 1)
                ]
            with m.If(bit_cnt == 0):
                m.d.sync += [
                    sending.eq(0),
                    self.tx.tx.eq(1)  # idle state
                    ]
        return m

if __name__ == "__main__":
    plat = ArtyA7_100Platform()
    dut  = UART32()
    plat.build(dut, do_program=True, do_build=True)
