from amaranth import *
from amaranth.sim import Simulator

from immbuilder import Immbuilder
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

immbuilder = Immbuilder()
sim = Simulator(immbuilder)
sim.add_clock(1e-6)  # 1 MHz clock

# Test instructions
test_instructions = [
    0x00A10093,        # I_type isALUImm    OK        rd = 1, rs1 = 2, imm = 10, funct3 = 0
    
    0x00312223,        # S-type isStore     OK           rs1 = 2, rs2 = 3, imm = 8, funct3 = 2                 funct7 and rd not used
    
    0x00208663,        # B-type isBranch    OK        rs1 = 1, rs2 = 2, imm = 12, funct3 = 0                funct7 and rd not used
    0x12345037,        # U-type isLUI       OK           rd = 0, imm = 305,418,240                             funct3, funct 7, rs1 and rs2 not used
    0x020000EF,        # J-type isJAL       OK           rd = 1, imm = 32                                      funct3, funct7, rs1 and rs2 not used
    
    # 0x00000073,        # isSystem       System ecall imm = 0, funct3 = 0, funct7 = 0                       rd, rs1 and rs2 not used
]

async def proc(ctx):
    
    ctx.set(immbuilder.instr.instr, test_instructions[1])  # Set the instruction to be decoded
    
    ctx.set(immbuilder.instr_flags.isStore, 1)


    print("instr   :", hex(ctx.get(immbuilder.instr.instr)))
    print("Immediate Data:", ctx.get(immbuilder.imm_data.imm))
    print("isALUimm:", (ctx.get(immbuilder.instr_flags.isALUimm)))
    print("isJALR :", (ctx.get(immbuilder.instr_flags.isJALR)))
    print("isLoad :", (ctx.get(immbuilder.instr_flags.isLoad)))
    print("isBranch:", (ctx.get(immbuilder.instr_flags.isBranch)))
    print("isLUI  :", (ctx.get(immbuilder.instr_flags.isLUI)))
    print("isAUIPC:", (ctx.get(immbuilder.instr_flags.isAUIPC)))
    print("isJAL  :", (ctx.get(immbuilder.instr_flags.isJAL)))
    print("isALUreg:", (ctx.get(immbuilder.instr_flags.isALUreg)))
    print("isStore:", (ctx.get(immbuilder.instr_flags.isStore)))
    print()

sim.add_testbench(proc)

with sim.write_vcd("immbuilder_isStore.vcd", "immbuilder_isStore.gtkw", traces=[
    immbuilder.instr.instr,
    immbuilder.instr_flags.isALUimm,
    immbuilder.instr_flags.isJALR,
    immbuilder.instr_flags.isLoad,
    immbuilder.instr_flags.isBranch,
    immbuilder.instr_flags.isLUI,
    immbuilder.instr_flags.isAUIPC,
    immbuilder.instr_flags.isJAL,
    immbuilder.instr_flags.isALUreg,
    immbuilder.instr_flags.isStore,
    immbuilder.imm_data.imm,
]):
    sim.run_until(36*10*1e-6)