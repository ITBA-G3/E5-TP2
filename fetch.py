from amaranth import *
from bus_signatures import fetch_decode, fetch_operand_b, pc_update
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
# remember to do platform imports here 

class Fetch(wiring.Component):
        # self.clk = ClockSignal()
        # i think i can use the sync domain's ClockSignal
   
    instr : Out(fetch_decode())
    pc : Out(fetch_operand_b()) 
    resetn : In(1)
    pc_update : In(pc_update())
    enable : In(1)

    def elaborate(self, platform):
        m = Module()
        self.n = 25
        program = [
            0b0000000_00000_00001_000_00000_0000000,    # nop
            # 0x3e800093,    # addi x1, x0, 1000
            # 0x3e900093,    # addi x1, x0, 1001
            # 0x3ea00093,    # addi x1, x0, 1002
            # 0x3e800093,    # addi x1, x0, 1000
            # 0x3e900093,    # addi x1, x0, 1001
            # 0x3ea00093,    # addi x1, x0, 1002
            # # -------------------------------
            # 0xfe208ee3,    # beq  x1, x2, -4
            # 0x3e800093,    # addi x1, x0, 1000
            # 0x3e900093,    # addi x1, x0, 1001
            # 0x3ea00093,    # addi x1, x0, 1002
            # 0xfe101de3,     # bne x0, x1, -6
            # 0x3ea00093,    # addi x1, x0, 1002
            # 0x3e900093,    # addi x1, x0, 1001
            # 0x3e800093    # addi x1, x0, 1000
            
            #FIBONACCI
            0x01900193,    # addi x3,x0,25    1
            0x00200093,    # addi x1,x0,2    2
            0x00100113,    # addi x2,x0,1    3
            0x00200213,    # addi x4,x0,2    4
            0x00200293,    # addi x5,x0,2    5
            0x0030d363,    # bge  x1,x3,6    6
            0x00208233,    # add x4,x1,x2    7
            0x00008133,    # add x2,x1,x0    8
            0x000200b3,    # add x1,x4,x0    9
            0x00128293,    # addi x5,x5,1    10
            0x00328263,    # beq x5,x3,4    11
            0xfe329de3,    # bne x5,x3,-6    12
            0x000103b3,    # add x7,x2,x0    13
            0x00a0006f,    # jal x0,10    14
            0x00000033,    # add x0,x0,x0    15
            0x000203b3,    # add x7,x4,x0    16
            0x00a0006f     # jal x0,10    17
        ]

        # 256-word 32-bit wide instr mem
        mem = Memory(width=32, depth=256, init=program +
        [0b0000000_00000_00001_000_00000_0000000]*(256-len(program)),
        attrs={"ram_style": "block"}) # NOP pad the rest


        rdport = mem.read_port()
        m.submodules.rdport = rdport

        with m.If(~self.resetn & self.enable):
            m.d.comb += [
                self.pc.pc.eq(self.pc_update.pc),        
                self.instr.instr.eq(rdport.data)
            ]
        
        with m.Elif(~self.enable):
            m.d.comb += [ self.pc.pc.eq(self.pc.pc)]

        m.d.comb += rdport.addr.eq(self.pc.pc)

        return m
