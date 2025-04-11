# cis511-ram-interpreter
## Overview

This repository contains a RAM (Random Access Machine) interpreter implementation and two example RAM programs demonstrating string manipulation:

1. `ram_interpreter.py`: The RAM interpreter implementation
2. `b3.1.py`: A program that reverses a string (computes f(w) = w^R)
3. `b3.2.py`: A program that triples a string (computes f(w) = www)

## RAM Machine Specification

The RAM machine operates with the following components:

- A set of registers (indexed from 1)
- An alphabet of symbols (e.g. {1,2} for an alphabet of length 2)
- A program consisting of instructions with 5 fields: [Label, X, Opcode, j, Y]

The RAM machine supports the following opcodes:

| Opcode | Description |
|--------|-------------|
| ADD | Append symbol j to register Y |
| TAIL | Remove first symbol from register Y |
| CLR | Clear register X |
| ASSIGN | Copy contents of register Y to register X |
| GOTOA | Unconditional jump above (to a label that appears earlier in the program) |
| GOTOB | Unconditional jump below (to a label that appears later in the program) |
| JMPA | Conditional jump above (to an earlier label if first symbol of X equals j) |
| JMPB | Conditional jump below (to a later label if first symbol of X equals j) |
| CONTINUE | Halt the program |

## Running the Programs

To run the example RAM programs, use the following commands:

```bash
# Run the string reversal RAM program
python3 b3.1.py

# Run the string tripling RAM program
python3 b3.2.py
```

Each program contains several test cases and will display the input, expected output, actual output, and whether the test passed.
