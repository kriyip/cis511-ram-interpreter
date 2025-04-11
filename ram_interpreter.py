from enum import IntEnum

class Opcode(IntEnum):
    """RAM machine opcodes"""
    ADD = 1      # Append symbol j to register Y
    TAIL = 2     # Remove first symbol from register Y
    CLR = 3      # Clear register X
    ASSIGN = 4   # Copy contents of register Y to register X
    GOTOA = 5    # Unconditional jump above (to a label that appears earlier in the program)
    GOTOB = 6    # Unconditional jump below (to a label that appears later in the program)
    JMPA = 7     # Conditional jump above (to an earlier label if first symbol of X equals j)
    JMPB = 8     # Conditional jump below (to a later label if first symbol of X equals j)
    CONTINUE = 9     # Halt the program

def RAMinterp(RAMprog, n, p, k, indata):
    """
    Executes a RAM program using a 1-indexed program counter.
    
    Parameters:
      RAMprog: list of instructions, each instruction is [label, X, opcode, j, Y]
      n: number of input registers (registers 1..n get the input strings)
      p: total number of registers (registers 1..p)
      k: alphabet size (symbols are assumed to be among {1,...,k})
      indata: list of input strings (each a list of symbols)
    
    Returns a tuple:
      (result, final_pc, final_registers, trace)
      
    Where:
      - result is the content of register 1 (program output)
      - final_pc is the final program counter (1-indexed)
      - final_registers is a list of registers 1..p
      - trace is a list of (pc, registers snapshot) recorded at each step.
    """
    
    # Validate that the input strings are in the alphabet {1,...,k}
    for i, string in enumerate(indata, start=1):
        for symbol in string:
            if not (1 <= symbol <= k):
                raise ValueError(f"Symbol {symbol} in w{i} is not in the alphabet 1..{k}, halting execution.")

    # Build label mapping: label -> (1-indexed) instruction number.
    label_to_pc = {}
    for index, instruction in enumerate(RAMprog):
        label = instruction[0]
        if label >= 0:
            if label in label_to_pc:
                raise ValueError("Duplicate label: {}".format(label))
            label_to_pc[label] = index + 1  # convert to 1-indexed
    
    registers = [None] * (p + 1)  # registers[0] is unused placeholder
    for i in range(1, p + 1):
        if i <= n:
            registers[i] = list(indata[i - 1])  # copy input string
        else:
            registers[i] = []
    
    pc = 1 # start program counter at 1
    trace = []  # stores (pc, registers[1:]) at each step
    steps = 0
    max_steps = 10000  # stop from running infinitely if something goes wrong

    while True:
        # record the current state in the trace
        trace.append((pc, [reg.copy() for reg in registers[1:]]))
        
        # validate pc (1-indexed valid range is 1 to len(RAMprog))
        if pc < 1 or pc > len(RAMprog):
            print("Program counter out of range. Halting execution.")
            break
        
        # get the current instruction (pc is 1-indexed)
        label, X, opcode, j, Y = RAMprog[pc - 1]
        
        if opcode == Opcode.ADD:  # add: Append symbol j to register Y.
            # Validate that the symbol being added is in the alphabet
            if not (1 <= j <= k):
                print("ADD ERROR: Symbol {} is not in the alphabet 1..{}".format(j, k))
                break
            registers[Y].append(j)
            pc += 1
            
        elif opcode == Opcode.TAIL:  # tail: Remove the first symbol from register Y
            if registers[Y]:
                registers[Y].pop(0)
            pc += 1
            
        elif opcode == Opcode.CLR:  # clr: Clear register X.
            registers[X] = []
            pc += 1
            
        elif opcode == Opcode.ASSIGN:  # assign: Copy contents of register Y to register X.
            registers[X] = registers[Y].copy()
            pc += 1
            
        elif opcode == Opcode.GOTOA:  # gotoa: Unconditional jump to an earlier label
            if Y in label_to_pc:
                target_pc = label_to_pc[Y]
                if target_pc >= pc:
                    print(f"GOTOA ERROR: Target label {Y} (pc={target_pc}) is not before current pc={pc}")
                    break
                pc = target_pc
            else:
                print("Jump target label {} not found. Halting execution.".format(Y))
                break
                
        elif opcode == Opcode.GOTOB:  # gotob: Unconditional jump to a later label
            if Y in label_to_pc:
                target_pc = label_to_pc[Y]
                if target_pc <= pc:
                    print(f"GOTOB ERROR: Target label {Y} (pc={target_pc}) is not after current pc={pc}")
                    break
                pc = target_pc
            else:
                print("Jump target label {} not found. Halting execution.".format(Y))
                break
                
        elif opcode == Opcode.JMPA:  # jmpa: Conditional jump to an earlier label
            if registers[X] and registers[X][0] == j:
                if Y in label_to_pc:
                    target_pc = label_to_pc[Y]
                    if target_pc >= pc:
                        print(f"JMPA ERROR: Target label {Y} (pc={target_pc}) is not before current pc={pc}")
                        break
                    pc = target_pc
                else:
                    print("Jump target label {} not found. Halting execution.".format(Y))
                    break
            else:
                pc += 1
                
        elif opcode == Opcode.JMPB:  # jmpb: Conditional jump to a later label
            if registers[X] and registers[X][0] == j:
                if Y in label_to_pc:
                    target_pc = label_to_pc[Y]
                    if target_pc <= pc:
                        print(f"JMPB ERROR: Target label {Y} (pc={target_pc}) is not after current pc={pc}")
                        break
                    pc = target_pc
                else:
                    print("Jump target label {} not found. Halting execution.".format(Y))
                    break
            else:
                pc += 1
                
        elif opcode == Opcode.CONTINUE:  # continue: Halt the program
            break
            
        else:
            print("Unknown opcode {} encountered. Halting execution.".format(opcode))
            break
        
        steps += 1
        if steps > max_steps:
            print("Maximum step count exceeded. Halting to avoid infinite loop.")
            break

    result = registers[1] # program output is in register 1
    final_pc = pc  # this is already 1-indexed
    final_registers = registers[1:]  # registers 1..p

    return result, final_pc, final_registers, trace
