from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out, connect
from amaranth_boards import arty_a7

from decoder import Decoder
from immbuilder import Immbuilder
from addrbuilder_jmpctrl import Addrbuilder

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
        

        self.decoder = decoder
        self.immbuilder = immbuilder
        self.addrbuilder = addrbuilder


        connect(m, decoder.alu_flags, immbuilder.instr_flags)
        connect(m, decoder.alu_flags, addrbuilder.instr_flags)

        connect(m, immbuilder.imm_data, addrbuilder.imm_data)

        return m