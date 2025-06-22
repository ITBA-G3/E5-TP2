from amaranth import *
from amaranth.sim import Simulator

from decoder import Decoder
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

decoder = Decoder()
sim = Simulator(decoder)
sim.add_clock(1e-6)  # 1 MHz clock

# Test instructions
test_instructions = [
    ("R-type: add x1, x2, x3",  0x003100B3),        # rd = 1, rs1 = 2, rs2 = 3, funct3 = 0, funct7 = 0      imm not used
    
    ("I-type: addi x1, x2, 10", 0x00A10093),        # rd = 1, rs1 = 2, imm = 10, funct3 = 0                 funct7 and rs2 not used
    ("S-type: sw x3, 0(x2)",    0x00312023),        # rs1 = 2, rs2 = 3, imm = 8, funct3 = 2                 funct7 and rd not used
    
    ("B-type: beq x1, x2, 12",  0x00208663),        # rs1 = 1, rs2 = 2, imm = 12, funct3 = 0                funct7 and rd not used
    ("U-type: lui x0, 0x12345", 0x12345037),        # rd = 0, imm = 305,418,240                             funct3, funct 7, rs1 and rs2 not used
    ("J-type: jal x1, 32",      0x020000EF),        # rd = 1, imm = 32                                      funct3, funct7, rs1 and rs2 not used
    
    ("System: ecall",           0x00000073),        # imm = 0, funct3 = 0, funct7 = 0                       rd, rs1 and rs2 not used
]

async def proc(ctx):
    for name, instr_aux in test_instructions:
        print(f"\n--- {name} ---")

        ctx.set(decoder.instr.instr, instr_aux)  # Set the instruction to be decoded

        print("instr   :", hex(ctx.get(decoder.instr.instr)))
        print("isALUreg:", (ctx.get(decoder.alu_flags.isALUreg)))
        print("isALUimm:", (ctx.get(decoder.alu_flags.isALUimm)))
        print("isBranch:", (ctx.get( decoder.alu_flags.isBranch)))
        print("isJALR  :", (ctx.get( decoder.alu_flags.isJALR)))
        print("isJAL   :", (ctx.get( decoder.alu_flags.isJAL)))
        print("isAUIPC :", (ctx.get( decoder.alu_flags.isAUIPC)))
        print("isLUI   :", (ctx.get( decoder.alu_flags.isLUI)))
        print("isLoad  :", (ctx.get( decoder.alu_flags.isLoad)))
        print("isStore :", (ctx.get( decoder.alu_flags.isStore)))
        print("isSystem:", (ctx.get( decoder.isSystem)))
    
        
        print("rdId    :", (ctx.get(decoder.reg_addr.rd_addr)))
        print("rs1Id   :", (ctx.get(decoder.reg_addr.rs1_addr)))
        print("rs2Id   :", (ctx.get(decoder.reg_addr.rs2_addr)))
        
        print("funct3  :", (ctx.get(decoder.functions.func3)))
        print("funct7  :", (ctx.get(decoder.functions.func7)))
        
        print()

sim.add_testbench(proc)

with sim.write_vcd("decoder.vcd", "decoder.gtkw", traces=[
    decoder.instr, decoder.alu_flags.isALUreg, decoder.alu_flags.isALUimm,
    decoder.alu_flags.isLoad, decoder.alu_flags.isStore, decoder.isSystem,
    decoder.reg_addr.rd_addr, decoder.reg_addr.rs1_addr, decoder.reg_addr.rs2_addr,
    decoder.functions.func3, decoder.functions.func7
]):
    sim.run_until(36*10*1e-6)