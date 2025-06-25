# Este código calcula el n-ésimo término de la serie de Fibonacci
lui t0, 0x80000
addi t1, x0, 10 # N: cantidad de términos

addi t2, x0, 0 # primer término
addi t3, x0, 1 # segundo término

addi t4, x0, 2 # contador de términos

loop:
    blt t1, t4, end
    add t5, t2, t3
    addi t2, t3, 0
    addi t3, t5, 0
    addi t4, t4, 1
    jal x0, loop

end:
    sb t3, 0(t0)