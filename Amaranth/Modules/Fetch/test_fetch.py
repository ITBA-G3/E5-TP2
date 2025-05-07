from amaranth import *
from amaranth.sim import Simulator, Settle
from fetch import Fetch

fetch = Fetch()

sim = Simulator(fetch)
sim.add_clock(1e-6)  # 1 MHz clock

def proc():
    yield fetch.resetn.eq(0)
    yield
    yield fetch.resetn.eq(1)

    for _ in range(10):
        yield
        yield Settle()

sim.add_sync_process(proc)

with sim.write_vcd("fetch.vcd", "fetch.gtkw", traces=[fetch.pc, fetch.instr, fetch.resetn]):
    sim.run()

