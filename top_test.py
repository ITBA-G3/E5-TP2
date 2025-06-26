from amaranth import *
from amaranth.sim import Simulator
from top import Top

top = Top()

async def proc(ctx):
    
    # ctx.set(top.fetch.resetn, 1)  # Reset the fetch module
    await ctx.tick()  # Initial tick to process the reset
    # ctx.set(top.fetch.resetn, 0)

    # ctx.set(top.fetch.resetn, 0)

    # ctx.set(top.opbuilder.muxes.muxA, 0)    # A = rs1
    # ctx.set(top.opbuilder.muxes.muxB, 0)    # B = rs2
    # ctx.set(top.pipeline.fetch_enable,1)
    # ctx.set(top.pipeline.decode_enable,1)
    # ctx.set(top.pipeline.retire_enable,1)
    # ctx.set(top.pipeline.execute_enable,1)
    # ctx.set(top.pipeline.addr_builder_enable,1)
    
    
    # ctx.set(top.regbank.we, 1)
    
    await ctx.tick().repeat(2)
    # print("-------JAL--------------")
    # print("instr: {:032b}".format(ctx.get(top.decoder.instr.instr)))
    # print("------------------------")
    # print(f"alu_A: {ctx.get(top.alu.data_buses.A)}")
    # print(f"alu_B: {ctx.get(top.alu.data_buses.B)}")
    await ctx.tick() # NOP -> estaba en la memoria del fetch
    # print("------------------------")
    # print(f"rs1_addr: {ctx.get(top.regbank.reg_addr.rs1_addr)}")
    # print(f"rs1_data: {ctx.get(top.regbank.rs_buses.rs1_data)}")
    # print(f"rs2_addr: {ctx.get(top.regbank.reg_addr.rs2_addr)}")
    # print(f"rs2_data: {ctx.get(top.regbank.rs_buses.rs2_data)}")
    # print("------------------------")
    # print(f"rd_addr: {ctx.get(top.regbank.reg_addr.rd_addr)}")
    # print(f"rd_data: {ctx.get(top.regbank.rd_bus.rd_data)}")
    
    # ctx.set(top.opbuilder.muxes.muxB, 0b001)    # B = rs2    

    await ctx.tick() # ADDI
    # print("-------ADDI: I = 7------")
    # print("instr: {:032b}".format(ctx.get(top.decoder.instr.instr)))
    # print("------------------------")
    # print(f"opbuild_imm: {ctx.get(top.opbuilder.imm.Iimm)}")
    # print(f"alu_A: {ctx.get(top.alu.data_buses.A)}")
    # print(f"alu_B: {ctx.get(top.alu.data_buses.B)}")
    await ctx.tick() #ADD
    # print("------------------------")
    # print(f"rs1_addr: {ctx.get(top.regbank.reg_addr.rs1_addr)}")
    # print(f"rs1_data: {ctx.get(top.regbank.rs_buses.rs1_data)}")
    # print(f"rs2_addr: {ctx.get(top.regbank.reg_addr.rs2_addr)}")
    # print(f"rs2_data: {ctx.get(top.regbank.rs_buses.rs2_data)}")
    # print("------------------------")
    # print(f"rd_addr: {ctx.get(top.regbank.reg_addr.rd_addr)}")
    # print(f"rd_data: {ctx.get(top.regbank.rd_bus.rd_data)}")


    
    
    

sim = Simulator(top)
sim.add_clock(1e-6)
sim.add_testbench(proc)

with sim.write_vcd('top_test.vcd'):
    sim.run_until(50 * 1e-6)  # Run for 20 ms