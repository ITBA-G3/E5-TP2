from amaranth import *
from amaranth.sim import Simulator

from addrbuilder_jmpctrl import Addrbuilder
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

addrbuilder = Addrbuilder()
sim = Simulator(addrbuilder)
sim.add_clock(1e-6)  # 1 MHz clock

# JAL val imm como offset       OK
# JALR val rs1 + imm como offset OK
# BRANCH val pc + imm como offset   OK

async def proc(ctx):
    
    ctx.set(addrbuilder.PC_in.pc, 1)  # Set the instruction to be decoded
    
    ctx.set(addrbuilder.imm_data.imm, 9)  # Set the immediate data for the instruction

    # TEST JAL JALR and Branch Instructions
    ctx.set(addrbuilder.instr_flags.isBranch, 1)

    ctx.set(addrbuilder.rs_data.rs1_data, 5)  # Set rs1 data to 5 for JALR test


    print("PC in   :", ctx.get(addrbuilder.PC_in.pc))
    # print("isJAL   :", hex(ctx.get(addrbuilder.instr_flags.isJAL)))
    # print("isJALR  :", hex(ctx.get(addrbuilder.instr_flags.isJALR)))
    print("isBranch:", hex(ctx.get(addrbuilder.instr_flags.isBranch)))
    
    print("imm:    :", ctx.get(addrbuilder.imm_data.imm))
    print("PC out  :", ctx.get(addrbuilder.PC_out.pc))
    print()

sim.add_testbench(proc)

with sim.write_vcd("addrbuilder_isBranch.vcd", "addrbuilder_isBranch.gtkw", traces=[
    addrbuilder.PC_in.pc,
    addrbuilder.PC_out.pc,
    addrbuilder.instr_flags.isJAL,
    addrbuilder.instr_flags.isJALR,
    addrbuilder.instr_flags.isBranch,
    addrbuilder.imm_data.imm,
]):
    sim.run_until(36*10*1e-6)