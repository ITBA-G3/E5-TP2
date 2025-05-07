from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

import os
import sys

from signatures_test import decode_alu_flags, operand_b_mux

from decoder import Decoder
from alu import ALU
from regbank import RegBank


class Fsm(wiring.Component):

    dec_flags: In(decode_alu_flags())
    incr_pc: Out(1)
    pc_enable: Out(1)
    muxes: Out(operand_b_mux())

    def __init__(self):
        super().__init__()
    
    def elaborate(self, platform):
        m = Module()
        with m.FSM(reset= "FETCH_INSTR") as fsm:
            with m.State("FETCH_INSTR"):
                #buscar instrucción de la memoria
                m.d.comb += self.incr_pc.eq(0)
                with m.If(self.dec_flags.isBranch):
                    m.next("BRANCH_1")
                with m.Elif(self.dec_flags.isALUreg | self.dec_flags.isALUimm):
                    m.next("SINGLE_CYCLE")
                with m.Elif(self.dec_flags.isLoad | self.dec_flags.isStore):
                    m.next("READ_STORE_1")
                with m.Elif(self.dec_flags.isJALR |self.dec_flags.isJAL | self.dec_flags.isAUIPC | self.dec_flags.isLUI):
                    m.next("PROXIMAMENTE")

            with m.State("BRANCH_1"):
                #primer paso de branches
                #reg <- PC+1 ; PC <- PC + Imm
                #paso 1: A = PC, B = 1, rd_addr = reg_addr, fun3 y fun7 para rd=A+1
                #paso 2: A = PC, B = Imm, rd_addr = PC
                m.next("BRANCH_2")

            with m.State("BRANCH_2"):
                #ultimo paso de branches
                m.d.comb += self.incr_pc.eq(1)
                m.next("FETCH_INSTR")


            with m.State("SINGLE_CYCLE"): #TODO: Falta considerar los casos de shamt
                m.d.comb += self.muxes.muxA.eq(0)
                with m.If(self.dec_flags.isImm):
                    m.d.comb += self.muxes.muxB.eq(0b001) #case Iimm
                m.d.comb += self.incr_pc.eq(1)
                m.next("FETCH_INSTR")


            with m.State("READ_STORE_1"):
                m.d.comb += self.muxes.muxA.eq(0) #ALU receives rs1
                with m.If(self.dec_flags.isStore):
                    m.d.comb += self.muxes.muxB.eq(0b011) #case  Simm when saving
                with m.Else():
                    m.d.comb += self.muxes.muxB.eq(0b001) #case Iimm when reading
                m.next("READ_STORE_2")

            with m.State("READ_STORE_2"):
                m.d.comb += self.incr_pc.eq(1)
                m.next("FETCH_INSTR")

            with m.State("PROXIMAMENTE"):
                m.d.comb += self.incr_pc.eq(1)
                m.next("FETCH_INSTR")

        # :)

        return m