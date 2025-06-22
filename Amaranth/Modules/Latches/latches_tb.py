from amaranth import *
from amaranth.sim import Simulator
from decode_latch import Decode_latch
# from top import Top

class Tumama (Elaboratable):
    def __init__(self):
        super().__init__()

    def elaborate(self, platform):
        m = Module()
        m.submodules.decode = decode = Decode_latch()
        self.decode = decode
        return m

tumama = Tumama()

async def proc(ctx):
    ctx.set(tumama.decode.decode_enable, 1)
    ctx.set(tumama.decode.decode_mux, 0)
    ctx.set(tumama.decode.instr_flags_in.isALUreg,1)
    print(ctx.get(tumama.decode.instr_flags_out.isALUreg))
    
    await ctx.tick()
    print(ctx.get(tumama.decode.instr_flags_out.isALUreg))
    ctx.set(tumama.decode.decode_mux, 1)
    await ctx.tick()
    print(ctx.get(tumama.decode.instr_flags_out.isALUreg))

sim = Simulator(tumama)
sim.add_clock(1e-6)  # 1 MHz clock
sim.add_testbench(proc)

with sim.write_vcd('latch.vcd'):
    sim.run_until(10 * 1e-6)  # Run for 20 ms