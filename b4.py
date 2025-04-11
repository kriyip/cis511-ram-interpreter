# RAM program to concatenate two strings
from ram_interpreter import RAMinterp, Opcode

RAMconcat = [
    [-1, 3, 4, 0, 1],   # assign: reg3 := reg1 (copy input string 1)
    [-1, 4, 4, 0, 2],   # assign: reg4 := reg2 (copy input string 2)
    [ 0, 4, 8, 1, 1],   # jmpb: if first symbol of reg4 == 1, jump to label 1
    [-1, 4, 8, 2, 2],   # jmpb: if first symbol of reg4 == 2, jump to label 2
    [-1, 0, 6, 0, 3],   # gotob: jump to label 3 (when reg4 is empty)
    [ 1, 0, 1, 1, 3],   # add: add symbol 1 to reg3 (label 1)
    [-1, 0, 2, 0, 4],   # tail: remove first symbol from reg4
    [-1, 0, 5, 0, 0],   # gotoa: jump to label 0 (back to test)
    [ 2, 0, 1, 2, 3],   # add: add symbol 2 to reg3 (label 2)
    [-1, 0, 2, 0, 4],   # tail: remove first symbol from reg4
    [-1, 0, 5, 0, 0],   # gotoa: jump to label 0
    [ 3, 1, 4, 0, 3],   # assign: copy reg3 into reg1 (store result in output register)
    [-1, 0, 9, 0, 0]    # continue: halt execution
]
    

indata1 = [
    [1, 2, 1, 2],
    [2, 1, 2, 1, 1, 2, 2]
]

result, final_pc, final_registers, trace = RAMinterp(RAMconcat, n=2, p=4, k=2, indata=indata1)


print("Input strings:")
for i, s in enumerate(indata1, start=1):
    print("  w{} = {}".format(i, s))

print("\nComputed function result (contents of register 1):")
print("  Result =", result)

print("\nExecution trace (pc, registers 1..p):")
for step, (pc_val, regs_snapshot) in enumerate(trace):
    print("  Step {}: pc = {:2d}, registers = {}".format(step, pc_val, regs_snapshot))
