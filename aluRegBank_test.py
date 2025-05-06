from amaranth import *
from amaranth.sim import Simulator
from aluRegBank import Top

top = Top()

async def proc(ctx):
    ctx.set(top.regbank.we, 1)
    ctx.set(top.alu.isALUreg, 0)
    ctx.set(top.alu.isALUimm, 0)
    ctx.set(top.alu.isJAL, 1)
    ctx.set(top.regbank.rs1_addr, 0)
    ctx.set(top.regbank.rs2_addr, 1)
    ctx.set(top.regbank.rd_addr, 2)
    ctx.set(top.alu.func7, 0)
    ctx.set(top.alu.func3, 0)
    await ctx.tick()
    ctx.set(top.regbank.rs1_addr, 2)
    print(ctx.get(top.regbank.reg_buses.rs1_data))

sim = Simulator(top)
sim.add_clock(1e-6)
sim.add_testbench(proc)

with sim.write_vcd('aluRegbank_test.vcd'):
    sim.run_until(10 * 1e-6)  # Run for 20 ms