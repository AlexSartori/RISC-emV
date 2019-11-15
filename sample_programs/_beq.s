addi x9, x0, 3
addi x10, x0, 18

beq x9, x9, 12

sw x9, 8(x10)
lw x11, 8(x10)

add x12, x9, x10