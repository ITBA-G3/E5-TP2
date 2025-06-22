from amaranth import *
from amaranth.sim import Simulator
from decode_latch import Decode_latch

dut = Decode_latch()

async def proc(ctx):

    ctx.set(dut.decode_mux, 1)
    ctx.set(dut.decode_enable, 0)

    ctx.set(dut.instr_flags_out.isJAL, 1)

    ctx.set(dut.instr_flags_in.isALUreg, 1)
    ctx.set(dut.instr_flags_in.isALUimm, 1)
    ctx.set(dut.instr_flags_in.isBranch, 1)
    ctx.set(dut.instr_flags_in.isJALR, 1)
    ctx.set(dut.instr_flags_in.isJAL, 1)
    ctx.set(dut.instr_flags_in.isAUIPC, 1)
    ctx.set(dut.instr_flags_in.isLUI, 1)
    ctx.set(dut.instr_flags_in.isLoad, 1)
    ctx.set(dut.instr_flags_in.isStore, 1)

    await ctx.tick()

    ctx.set(dut.decode_mux, 0)
    ctx.set(dut.decode_enable, 1)

    ctx.set(dut.instr_flags_in.isALUreg, 1)
    ctx.set(dut.instr_flags_in.isALUimm, 1)
    ctx.set(dut.instr_flags_in.isBranch, 1)
    ctx.set(dut.instr_flags_in.isJALR, 1)
    ctx.set(dut.instr_flags_in.isJAL, 1)
    ctx.set(dut.instr_flags_in.isAUIPC, 1)
    ctx.set(dut.instr_flags_in.isLUI, 1)
    ctx.set(dut.instr_flags_in.isLoad, 1)
    ctx.set(dut.instr_flags_in.isStore, 1)

    await ctx.tick()



sim = Simulator(dut)
f = 1e6
sim.add_clock(1/f)
sim.add_testbench(proc)

with sim.write_vcd('tb_decode_latch.vcd'):
    sim.run_until(10 * 1/f)
