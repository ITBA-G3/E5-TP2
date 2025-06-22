from amaranth import *
from bus_signatures import decode_alu_flags, decode_reg_addr, fetch_decode, fetch_operand_b
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

class Pipeline(wiring.Component):

    instr_flags_fetch : In(decode_alu_flags())
    reg_addr_fetch : In(decode_reg_addr())

    instr_flags_decode : In(decode_alu_flags())
    reg_addr_decode : In(decode_reg_addr())

    instr_flags_execute : In(decode_alu_flags())
    rd_execute : In(5)

    instr_flags_retire : In(decode_alu_flags())
    rd_retire : In(5)

    fetch_enable : Out(1)
    fetch_mux : Out(1)

    decode_enable : Out(1)
    decode_mux : Out(1)
    
    execute_enable : Out(1)
    execute_mux : Out(1)
    
    retire_enable : Out(1)
    retire_mux : Out(1)

    addr_builder_mux: Out(1)
    addr_builder_enable : Out(1)


    def elaborate(self, platform):
        m = Module()

        #laputamadre qué casos tengo que considerarrrrr
        #si más de una etapa quiere usar el mismo registro, freno?
            #sí, siempre que sean etapas que no permitan el guardado de un registro y lo quieran usar con un valor anterior
            #ok gracias, la puta madre
            #Entonces acá la sección crítica es todo lo que está antes del operand builder.
        #habría que hacer una máquina de estados para saber dónde está la instrucción de salto?
        with m.If(self.instr_flags_execute.isALUreg and ((self.rd_execute == self.reg_addr_decode.rs1_addr) or (self.rd_execute == self.reg_addr_decode.rs2_addr))):
            #acá el rd de lo que se está ejecutando es igual al rs1 o rs2 de lo que se quiere ejecutar. Tengo que frenar hasta que se haya escrito
            m.d.comb += [self.fetch_enable.eq(0), self.decode_enable.eq(0)]
            m.d.comb += [self.fetch_mux.eq(0), self.decode_mux.eq(0), self.execute_mux.eq(0), self.retire_mux.eq(0)]
        with m.Elif():#acá pondría el caso en el que hay que limpiar el pipeline
            m.d.comb += [self.fetch_mux.eq(1), self.decode_mux.eq(1), self.execute_mux.eq(1), self.retire_mux.eq(1)]
        with m.Else(): #este caso es en el que ta to' normal
            m.d.comb += [self.fetch_mux.eq(0), self.decode_mux.eq(0), self.execute_mux.eq(0), self.retire_mux.eq(0)]
            m.d.comb += [self.fetch_enable.eq(1), self.decode_enable.eq(1), self.execute_enable.eq(1), self.retire_enable.eq(1)]
        return m