from amaranth import *

class RegBank (Elaboratable):
    def __init__(self):
        self.bank = Signal(32)
        pass

    def elaborate (self, platform):
        m = Module()
