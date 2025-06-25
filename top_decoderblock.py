from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out, connect
from amaranth_boards.arty_a7 import ArtyA7_100Platform

from decoder import Decoder
from immbuilder import Immbuilder
from addrbuilder_jmpctrl import Addrbuilder
from fetch import Fetch

class TopDecoderBlock (Elaboratable):

    def __init__(self):
        super().__init__()

    def elaborate(self, platform):
        m = Module()

        beep = Signal()
        m.d.sync += [beep.eq(beep + 1)]

        m.submodules.decoder = decoder = Decoder()
        m.submodules.immbuilder = immbuilder = Immbuilder()
        m.submodules.addrbuilder = addrbuilder = Addrbuilder()
        m.submodules.fetch = fetch = Fetch()
        

        self.decoder = decoder
        self.immbuilder = immbuilder
        self.addrbuilder = addrbuilder
        self.fetch = fetch


        connect(m, decoder.alu_flags, immbuilder.instr_flags)
        connect(m, decoder.alu_flags, addrbuilder.instr_flags)

        connect(m, immbuilder.imm_data, addrbuilder.imm_data)

        connect(m, fetch.pc, addrbuilder.PC_in)
        connect(m, addrbuilder.PC_out, fetch.pc_update)

        connect(m, fetch.instr, decoder.instr)
        connect(m, fetch.instr, immbuilder.instr)

        return m

if __name__ == "__main__":
    core = TopDecoderBlock()
    platform = ArtyA7_100Platform()
    platform.build(core, do_build=True, do_program=False)