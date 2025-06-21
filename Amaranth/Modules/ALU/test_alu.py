from amaranth import *
from amaranth.sim import Simulator
from alu import ALU

alu = ALU()

async def alu_tb(ctx):
    
    # ADD
    ctx.set(alu.A, 10)
    ctx.set(alu.B, 5)
    ctx.set(alu.func3, 0b000)
    ctx.set(alu.func7, 0b0000000)
    ctx.set(alu.isALUreg, 1)
    await ctx.tick()
    q = ctx.get(alu.Q)
    print(f"ADD: 10 + 5 = {q}")

    # SUB
    ctx.set(alu.func7, 0b0100000)
    await ctx.tick()
    q = ctx.get(alu.Q)
    print(f"SUB: 10 - 5 = {q}")

    # SLT
    ctx.set(alu.A, -5 & 0xFFFFFFFF)
    ctx.set(alu.B, 3)
    ctx.set(alu.func3, 0b010)
    ctx.set(alu.func7, 0)
    await ctx.tick()
    q = ctx.get(alu.Q)
    print(f"SLT: -5 < 3 = {q}")

    # SLTU
    ctx.set(alu.A, 0xFFFFFFFF)
    ctx.set(alu.B, 1)
    ctx.set(alu.func3, 0b011)
    await ctx.tick()
    q = ctx.get(alu.Q)
    print(f"SLTU: 0xFFFFFFFF < 1 = {q}")

    # AND
    ctx.set(alu.A, 0b1100)
    ctx.set(alu.B, 0b1010)
    ctx.set(alu.func3, 0b111)
    await ctx.tick()
    q = ctx.get(alu.Q)
    print(f"AND: 1100 & 1010 = {q:04b}")

    # OR
    ctx.set(alu.func3, 0b110)
    await ctx.tick()
    q = ctx.get(alu.Q)
    print(f"OR: 1100 | 1010 = {q:04b}")

    # SRL
    ctx.set(alu.A, 0b1000)
    ctx.set(alu.shamt, 2)
    ctx.set(alu.func3, 0b101)
    ctx.set(alu.func7, 0)
    await ctx.tick()
    q = ctx.get(alu.Q)
    print(f"SRL: 1000 >> 2 = {q:04b}")

    # SRA
    ctx.set(alu.A, (-8) & 0xFFFFFFFF)
    ctx.set(alu.shamt, 2)
    ctx.set(alu.func7, 0b0100000)
    await ctx.tick()
    q = ctx.get(alu.Q)
    print(f"SRA: -8 >>> 2 = {q:032b}")

sim = Simulator(alu)
sim.add_clock(1e-6, domain="sync")
sim.add_testbench(alu_tb)
with sim.write_vcd("alu.vcd"):
    sim.run()