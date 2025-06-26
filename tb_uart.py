from amaranth import *
from amaranth.sim import Simulator, Delay
from uart import UART32

def uart32_tb():
    dut = UART32()
    m = Module()
    m.submodules.dut = dut

    def process():
        for _ in range(5):
            yield

        print("READY before send:", (yield dut.ready))
        yield dut.data.eq(0xDEADBEEF)
        yield dut.send.eq(0)
        yield
        yield dut.send.eq(1)
        yield
        yield dut.send.eq(0)

        print("Transmitted bit-stream:")
        for _ in range(1600 * 10):  # 40 bits × 10 cycles/bit = 400 cycles
            # Only sample at the *start* of each bit-period
            if (yield (yield)) == 1: pass  # noop, just advance simulation
            # Actually, simplify: sample every 10th cycle
            if (_ % 10) == 0:
                print((yield dut.tx), end='')
            yield
        print("\nREADY after send:", (yield dut.ready))
    
    sim = Simulator(m)
    sim.add_clock(1e-6)            # period irrelevant for cycle-accurate sim
    sim.add_sync_process(process)
    with sim.write_vcd("uart32_tb.vcd"):
        sim.run()

if __name__ == "__main__":
    uart32_tb()