from ram_interpreter import RAMinterp, Opcode

# RAM program to compute f(w) = www (triples the input string)
RAMtriple = [
    # First, copy R1 to R2 and R3
    [-1, 2, Opcode.ASSIGN, 0, 1],   # Copy R1 to R2
    [-1, 3, Opcode.ASSIGN, 0, 1],   # Copy R1 to R3

    # First loop: append R2 to R1
    [10, 2, Opcode.JMPB, 1, 11],    # If first symbol of R2 is 1, jump to label 11
    [-1, 2, Opcode.JMPB, 2, 12],    # If first symbol of R2 is 2, jump to label 12
    [-1, 0, Opcode.GOTOB, 0, 20],   # If R2 is empty, jump to second loop at label 20

    # Handle symbol 1 from R2
    [11, 2, Opcode.TAIL, 0, 2],     # Remove first symbol (1) from R2
    [-1, 1, Opcode.ADD, 1, 1],      # Append symbol 1 to R1
    [-1, 0, Opcode.GOTOA, 0, 10],   # Jump back to first loop

    # Handle symbol 2 from R2
    [12, 2, Opcode.TAIL, 0, 2],     # Remove first symbol (2) from R2
    [-1, 1, Opcode.ADD, 2, 1],      # Append symbol 2 to R1
    [-1, 0, Opcode.GOTOA, 0, 10],   # Jump back to first loop

    # Second loop: append R3 to R1
    [20, 3, Opcode.JMPB, 1, 21],    # If first symbol of R3 is 1, jump to label 21
    [-1, 3, Opcode.JMPB, 2, 22],    # If first symbol of R3 is 2, jump to label 22
    [-1, 0, Opcode.GOTOB, 0, 30],   # If R3 is empty, jump to halt at label 30

    # Handle symbol 1 from R3
    [21, 3, Opcode.TAIL, 0, 3],     # Remove first symbol (1) from R3
    [-1, 1, Opcode.ADD, 1, 1],      # Append symbol 1 to R1
    [-1, 0, Opcode.GOTOA, 0, 20],   # Jump back to second loop

    # Handle symbol 2 from R3
    [22, 3, Opcode.TAIL, 0, 3],     # Remove first symbol (2) from R3
    [-1, 1, Opcode.ADD, 2, 1],      # Append symbol 2 to R1
    [-1, 0, Opcode.GOTOA, 0, 20],   # Jump back to second loop

    # Halt
    [30, 0, Opcode.CONTINUE, 0, 0]  # Halt the program
]

# Test cases
test_cases = [
    [],                 # Empty string -> empty string
    [1],                # 1 -> 111
    [2],                # 2 -> 222
    [1, 2],             # 12 -> 121212
    [2, 1],             # 21 -> 212121
    [1, 2, 1, 2]        # 1212 -> 121212121212
]

# Run tests
for input_string in test_cases:
    print(f"\nTesting input: {input_string}")
    result, final_pc, final_registers, trace = RAMinterp(RAMtriple, n=1, p=3, k=2, indata=[input_string])
    
    # Compute expected output (www)
    expected = input_string * 3
    
    print(f"Expected output: {expected}")
    print(f"Actual output: {result}")
    print(f"Correct: {result == expected}")
