from amaranth import *
from amaranth.sim import Simulator
from regbank import RegBank

regbank = RegBank()

counter = 0

async def proc(ctx):
    while True:
        yield regbank.rs1_addr.eq(2)
        salida = ctx.get_signal_value(regbank.rs1_data)
        print(f"rs1_data: {salida}")
        yield regbank.rd_addr.eq(2)
        yield regbank.rd_data.eq(counter)
        yield regbank.we.eq(1)
        counter += 1
        await ctx.tick()


sim = Simulator(regbank)
sim.add_clock(1e-6)  # 1 MHz clock
sim.add_testbench(proc)

with sim.write_vcd('regbank_test.vcd'):
    sim.run_until(2e-5)  # Run for 20 ms

