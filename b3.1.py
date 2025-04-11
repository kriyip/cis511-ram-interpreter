from ram_interpreter import RAMinterp, Opcode

# RAM program to reverse a string
RAMreverse = [
    # --- MAIN LOOP (Label 10) ---
    [10, 1, Opcode.JMPB, 1, 11],    # If first symbol of R1 is 1, jump to symbol 1 handler at label 11
    [-1, 1, Opcode.JMPB, 2, 12],     # If first symbol of R1 is 2, jump to symbol 2 handler at label 12
    [-1, 0, Opcode.GOTOB, 0, 13],    # If R1 is empty, jump to finish (label 13)

    # --- HANDLER FOR SYMBOL 1 (Label 11) ---
    [11, 1, Opcode.TAIL, 0, 1],      # Remove first symbol (1) from R1
    [-1, 3, Opcode.ASSIGN, 0, 2],    # Copy R2 to R3 (save R2's content)
    [-1, 2, Opcode.CLR, 0, 0],       # Clear R2
    [-1, 2, Opcode.ADD, 1, 2],       # Put 1 at start of R2

    # Copy-back loop for symbol 1 (Labels 20-23)
    [20, 3, Opcode.JMPB, 1, 21],     # If first symbol of R3 is 1, jump to label 21
    [-1, 3, Opcode.JMPB, 2, 22],     # If first symbol of R3 is 2, jump to label 22
    [-1, 0, Opcode.GOTOB, 0, 23],    # If R3 is empty, jump to label 23 to finish
    [21, 0, Opcode.TAIL, 0, 3],      # Remove symbol 1 from R3
    [-1, 0, Opcode.ADD, 1, 2],       # Append symbol 1 to R2
    [-1, 0, Opcode.GOTOA, 0, 20],    # Jump back to start of copy-back loop
    [22, 0, Opcode.TAIL, 0, 3],      # Remove symbol 2 from R3
    [-1, 0, Opcode.ADD, 2, 2],       # Append symbol 2 to R2
    [-1, 0, Opcode.GOTOA, 0, 20],    # Jump back to start of copy-back loop
    [23, 0, Opcode.GOTOA, 0, 10],    # Copy-back done, jump back to main loop

    # --- HANDLER FOR SYMBOL 2 (Label 12) ---
    [12, 1, Opcode.TAIL, 0, 1],      # Remove first symbol (2) from R1
    [-1, 3, Opcode.ASSIGN, 0, 2],    # Copy R2 to R3 (save R2's content)
    [-1, 2, Opcode.CLR, 0, 0],       # Clear R2
    [-1, 2, Opcode.ADD, 2, 2],       # Put 2 at start of R2

    # Copy-back loop for symbol 2 (Labels 30-33)
    [30, 3, Opcode.JMPB, 1, 31],     # If first symbol of R3 is 1, jump to label 31
    [-1, 3, Opcode.JMPB, 2, 32],     # If first symbol of R3 is 2, jump to label 32
    [-1, 0, Opcode.GOTOB, 0, 33],    # If R3 is empty, jump to label 33 to finish
    [31, 0, Opcode.TAIL, 0, 3],      # Remove symbol 1 from R3
    [-1, 0, Opcode.ADD, 1, 2],       # Append symbol 1 to R2
    [-1, 0, Opcode.GOTOA, 0, 30],    # Jump back to start of copy-back loop
    [32, 0, Opcode.TAIL, 0, 3],      # Remove symbol 2 from R3
    [-1, 0, Opcode.ADD, 2, 2],       # Append symbol 2 to R2
    [-1, 0, Opcode.GOTOA, 0, 30],    # Jump back to start of copy-back loop
    [33, 0, Opcode.GOTOA, 0, 10],    # Copy-back done, jump back to main loop

    # --- FINISH (Label 13) ---
    [13, 1, Opcode.ASSIGN, 0, 2],    # Copy R2 (reversed string) to R1
    [-1, 0, Opcode.CONTINUE, 0, 0]   # Halt
]

# Test cases
test_cases = [
    [],
    [1],
    [1, 2, 1, 2],
    [2, 1, 2, 1, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2],
]

# Run tests
for input_string in test_cases:
    print(f"\nTesting input: {input_string}")
    result, final_pc, final_registers, trace = RAMinterp(RAMreverse, n=1, p=3, k=2, indata=[input_string])
    print(f"Expected output: {input_string[::-1]}")
    print(f"Actual output: {result}")
    print(f"Correct: {result == input_string[::-1]}")