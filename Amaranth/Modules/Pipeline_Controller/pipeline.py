from amaranth import *
from bus_signatures import branch_flags, decode_alu_flags, decode_reg_addr, fetch_decode, fetch_operand_b
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

    branch_flags_execute : In(branch_flags())

    alu_flag_z : In(1)
    alu_flag_n : In(1)

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
        # m.d.comb += [self.fetch_enable.eq(1), self.decode_enable.eq(1), self.execute_enable.eq(1), self.retire_enable.eq(1), self.addr_builder_enable.eq(1)]

        with m.If(self.instr_flags_execute.isBranch):

            with m.If(self.branch_flags_execute.beq & ~self.alu_flag_z):
                #limpiar todo porque se saltó mal
                m.d.comb += [self.fetch_mux.eq(1), self.decode_mux.eq(1), self.execute_mux.eq(1), self.retire_mux.eq(1)]
                m.d.comb += self.addr_builder_mux.eq(1)

            with m.Elif(self.branch_flags_execute.bne & self.alu_flag_z):
                #limpiar todo porque se saltó mal
                m.d.comb += [self.fetch_mux.eq(1), self.decode_mux.eq(1), self.execute_mux.eq(1), self.retire_mux.eq(1)]
                m.d.comb += self.addr_builder_mux.eq(1)

            with m.Elif(self.branch_flags_execute.blt & ~self.alu_flag_n):
                #limpiar todo porque se saltó mal
                m.d.comb += [self.fetch_mux.eq(1), self.decode_mux.eq(1), self.execute_mux.eq(1), self.retire_mux.eq(1)]
                m.d.comb += self.addr_builder_mux.eq(1)

            with m.Elif(self.branch_flags_execute.bge & self.alu_flag_n):
                #limpiar todo porque se saltó mal
                m.d.comb += [self.fetch_mux.eq(1), self.decode_mux.eq(1), self.execute_mux.eq(1), self.retire_mux.eq(1)]
                m.d.comb += self.addr_builder_mux.eq(1)

            with m.Elif(self.branch_flags_execute.bltu & ~self.alu_flag_n):
                #limpiar todo porque se saltó mal
                m.d.comb += [self.fetch_mux.eq(1), self.decode_mux.eq(1), self.execute_mux.eq(1), self.retire_mux.eq(1)]
                m.d.comb += self.addr_builder_mux.eq(1)

            with m.Elif(self.branch_flags_execute.bgeu & self.alu_flag_n):
                #limpiar todo porque se saltó mal
                m.d.comb += [self.fetch_mux.eq(1), self.decode_mux.eq(1), self.execute_mux.eq(1), self.retire_mux.eq(1)]
                m.d.comb += self.addr_builder_mux.eq(1)
                m.d.comb += self.addr_builder_enable.eq(0)

        with m.Elif((self.instr_flags_decode.isALUreg | self.instr_flags_decode.isALUimm) & (self.instr_flags_execute.isALUreg | self.instr_flags_execute.isALUimm)):
            
            with m.If((self.reg_addr_decode.rs1_addr != 0) & (self.rd_execute != 0) &
                    ((self.rd_execute == self.reg_addr_decode.rs1_addr) | 
                     (self.rd_execute == self.reg_addr_decode.rs2_addr))):
            #acá el rd de lo que se está ejecut&o es igual al rs1 o rs2 de lo que se quiere ejecutar. Tengo que frenar hasta que se haya escrito
                m.d.comb += [self.fetch_enable.eq(0), self.decode_enable.eq(0), self.addr_builder_enable.eq(0), 
                             self.execute_enable.eq(0), self.retire_enable.eq(1)]
                
                m.d.comb += [self.fetch_mux.eq(0), self.decode_mux.eq(0), self.execute_mux.eq(1), 
                             self.retire_mux.eq(0), self.addr_builder_mux.eq(0)] #mux de decode, para meter NOP a execute

        with m.Else(): #este caso es en el que ta to' normal
            m.d.comb += [self.fetch_mux.eq(0), self.decode_mux.eq(0), self.execute_mux.eq(0), self.retire_mux.eq(0), self.addr_builder_mux.eq(0)]
            m.d.comb += [self.fetch_enable.eq(0), self.decode_enable.eq(1), self.execute_enable.eq(1), self.retire_enable.eq(1), self.addr_builder_enable.eq(1)]
        
        return m