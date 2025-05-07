from amaranth import *
from amaranth.sim import Simulator
from top import Top

top = Top()

async def proc(ctx):
    
    ctx.set(top.fetch.resetn, 0)
    # set operand build flags
    ctx.set(top.opbuilder.muxes.muxA, 0)    # A = rs1
    ctx.set(top.opbuilder.muxes.muxB, 0)    # B = rs2
    
    ctx.set(top.regbank.we, 1)
    
    
    # ctx.set(top.decoder.instr, 0b000000_00000_00001_000_00001_1101111)
    # ctx.set(top.alu.isALUreg, 0)
    # ctx.set(top.alu.isALUimm, 0)
    # ctx.set(top.alu.isJAL, 1)
    # ctx.set(top.regbank.rs1_addr, 0)
    # ctx.set(top.regbank.rs2_addr, 1)
    # ctx.set(top.regbank.rd_addr, 2)
    # ctx.set(top.alu.func7, 0)
    # ctx.set(top.alu.func3, 0)
    await ctx.tick().repeat(2)
    
    print("JAL harcoded in fetch -> expected 4 in rs1_data")
    print("instr: {:032b}".format(ctx.get(top.decoder.instr.instr)))
    print("------------------------")
    print(f"alu_A: {ctx.get(top.alu.data_buses.A)}")
    print(f"alu_B: {ctx.get(top.alu.data_buses.B)}")
    await ctx.tick()
    print("------------------------")
    print(f"rs1_addr: {ctx.get(top.regbank.reg_addr.rs1_addr)}")
    print(f"rs1_data: {ctx.get(top.regbank.rs_buses.rs1_data)}")
    print(f"rs2_addr: {ctx.get(top.regbank.reg_addr.rs2_addr)}")
    print(f"rs2_data: {ctx.get(top.regbank.rs_buses.rs2_data)}")
    print("------------------------")
    print(f"rd_addr: {ctx.get(top.regbank.reg_addr.rd_addr)}")
    print(f"rd_data: {ctx.get(top.regbank.rd_bus.rd_data)}")
    
    

sim = Simulator(top)
sim.add_clock(1e-6)
sim.add_testbench(proc)

with sim.write_vcd('aluRegbank_test.vcd'):
    sim.run_until(10 * 1e-6)  # Run for 20 ms