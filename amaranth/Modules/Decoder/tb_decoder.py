from amaranth import *
from amaranth.sim import Simulator, Settle
from decoder import Decoder

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

def proc():
    for name, instr in test_instructions:
        print(f"\n--- {name} ---")
        yield decoder.instr.eq(instr)
        yield Settle()

        # Print outputs
        print("instr   :", hex((yield decoder.instr)))
        print("isALUreg:", (yield decoder.isALUreg))
        print("isALUimm:", (yield decoder.isALUimm))
        print("isBranch:", (yield decoder.isBranch))
        print("isJALR  :", (yield decoder.isJALR))
        print("isJAL   :", (yield decoder.isJAL))
        print("isAUIPC :", (yield decoder.isAUIPC))
        print("isLUI   :", (yield decoder.isLUI))
        print("isLoad  :", (yield decoder.isLoad))
        print("isStore :", (yield decoder.isStore))
        print("isSystem:", (yield decoder.isSystem))
        
        print("rdId    :", (yield decoder.rdId))
        print("rs1Id   :", (yield decoder.rs1Id))
        print("rs2Id   :", (yield decoder.rs2Id))
        
        print("funct3  :", (yield decoder.funct3))
        print("funct7  :", (yield decoder.funct7))
        
        print("Iimm    :", (yield decoder.Iimm))
        print("Uimm    :", (yield decoder.Uimm))
        print("Simm    :", (yield decoder.Simm))
        print("Bimm    :", (yield decoder.Bimm))
        print("Jimm    :", (yield decoder.Jimm))
        print()

        yield   	# Wait for a clock cycle before the next instruction

sim.add_sync_process(proc)

with sim.write_vcd("decoder.vcd", "decoder.gtkw", traces=[
    decoder.instr, decoder.isALUreg, decoder.isALUimm,
    decoder.isLoad, decoder.isStore, decoder.isSystem,
    decoder.rdId, decoder.rs1Id, decoder.rs2Id,
    decoder.funct3, decoder.Iimm
]):
    sim.run()
