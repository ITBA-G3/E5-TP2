# Suma de los primeros N numeros naturales
lui t0, 0x80000 # memoria donde se guarda el resultado

addi t1, x0, 10 # N: limite de la suma
addi t2, x0, 0 # resultado
addi t3, x0, 1 # contador

loop:
    add t2, t2, t3 # t2 = t2 + t3
    addi t3, t3, 1 # t3 = t3 + 1 actualizo contador
    blt t1, t3, end
    jal x0, loop

end:
    sb t2, 0(t0) # guardo resultado