# Programa para verificar si un número es par o impar
lui t0, 0x80000

addi t1, x0, 10     # número que chequeo

andi t2, t1, 1      # verifico el último bit
beq t2, x0, even

addi t3, x0, 0      # es impar
sb t3, 0(t0)        # guarda un 0
jal x0, end

even:               # es par
    addi t3, x0, 1
    sb t3, 0(t0)    # guarda un 1

end:
    jal x0, end