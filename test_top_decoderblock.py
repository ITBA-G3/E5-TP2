from amaranth import *
from amaranth.sim import Simulator
from top_decoderblock import TopDecoderBlock

top = TopDecoderBlock()
sim = Simulator(top)
sim.add_clock(1e-6)  # 1 MHz clock

test_instructions = [
    0x00A10093,        # I_type isALUImm    OK        rd = 1, rs1 = 2, imm = 10, funct3 = 0                 funct7 and rs2 not used
    0x00312023,        # S-type isStore     BROKEN IMM         rs1 = 2, rs2 = 3, imm = 8, funct3 = 2                 funct7 and rd not used
    
    0x00208663,        # B-type isBranch    OK         rs1 = 1, rs2 = 2, imm = 12, funct3 = 0                funct7 and rd not used
    0x12345037,        # U-type isLUI       OK           rd = 0, imm = 305,418,240                             funct3, funct 7, rs1 and rs2 not used
    0x020000EF,        # J-type isJAL       OK           rd = 1, imm = 32            
                              
    # JALR instruction with imm = 5
    0x003100E7,        # I-type isJALR      OK           rd = 1, rs1 = 2, imm = 3, funct3 = 0 
                    # PC should increment by 2
                    
    0x004100E7      # I-type isJALR      OK           rd = 1, rs1 = 2, imm = 4, funct3 = 0                  
                    # funct7 and rs2 not used
                    # PC should increment by 4

    # 0x00000073,        # isSystem       System ecall imm = 0, funct3 = 0, funct7 = 0                       rd, rs1 and rs2 not used
]

async def proc(ctx):

    test_instr = test_instructions[6]  # Select the first instruction for testing

    ctx.set(top.decoder.instr.instr, test_instr)  # Set the instruction to be decoded
    ctx.set(top.immbuilder.instr.instr, test_instr)  # Set the instruction for imm builder

    ctx.set(top.addrbuilder.PC_in.pc, 0)  # Set initial PC value
    
    # ctx.set(top.addrbuilder.rs_data.rs1_data, 5)  # Set rs1 data FOR JALR INSTRUCTION
    
    await ctx.tick().repeat(2)  # Initial tick to process the inputs
    print("Instr :", hex(ctx.get(top.decoder.instr.instr)))
    print("PC In :", hex(ctx.get(top.addrbuilder.PC_in.pc)))
    print("PC Out:", ctx.get(top.addrbuilder.PC_out.pc))
    print("isALUreg :", ctx.get(top.addrbuilder.instr_flags.isALUreg))
    print("isALUimm :", ctx.get(top.addrbuilder.instr_flags.isALUimm))
    print("isLUI :", ctx.get(top.addrbuilder.instr_flags.isLUI))
    print("isAUIPC :", ctx.get(top.addrbuilder.instr_flags.isAUIPC))
    print("isBranch :", ctx.get(top.addrbuilder.instr_flags.isBranch))
    print("isJAL :", ctx.get(top.addrbuilder.instr_flags.isJAL))
    print("isJALR :", ctx.get(top.addrbuilder.instr_flags.isJALR))
    print("isStore :", ctx.get(top.addrbuilder.instr_flags.isStore))
    print("isLoad :", ctx.get(top.addrbuilder.instr_flags.isLoad))

    print("Imm Data :", ctx.get(top.addrbuilder.imm_data.imm))

    await ctx.tick()  # Initial tick to process the inputs


sim.add_testbench(proc)

with sim.write_vcd("test_top_decoderblock.vcd", "test_top_decoderblock.gtkw", traces=[
    top.addrbuilder.PC_out.pc,
    top.addrbuilder.PC_in.pc,
    top.addrbuilder.instr_flags.isALUreg,
    top.addrbuilder.instr_flags.isALUimm,
    top.addrbuilder.instr_flags.isLUI,
    top.addrbuilder.instr_flags.isAUIPC,
    top.addrbuilder.instr_flags.isBranch,
    top.addrbuilder.instr_flags.isJAL,
    top.addrbuilder.instr_flags.isJALR,
    top.addrbuilder.imm_data.imm,
    top.addrbuilder.rs_data.rs1_data
]):
    sim.run()