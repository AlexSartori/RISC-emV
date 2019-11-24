.text
  addi x1, x0, 0    ; counter
  addi x2, x0, 10   ; how many

loop:
  addi x1, x1, 1    ; counter++
  sw x1, 0(x1)      ; write to memory
  bne x1, x2, loop  ; loop if count != 10
