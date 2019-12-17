![Logo](logo.png)

[![Build Status](https://travis-ci.org/AlexSartori/RISC-emV.svg?branch=develop)](https://travis-ci.org/AlexSartori/RISC-emV) &nbsp;
[![codecov](https://codecov.io/gh/AlexSartori/RISC-emV/branch/develop/graph/badge.svg)](https://codecov.io/gh/AlexSartori/RISC-emV)
&nbsp;
[![CodeFactor](https://www.codefactor.io/repository/github/alexsartori/risc-emv/badge)](https://www.codefactor.io/repository/github/alexsartori/risc-emv)


Graphical emulator for the RISC-V architecture, implementing the Tomasulo algorithm and the Simultaneous Multi-Threading.



## Installation
From within the repository directory:
```
pip install -e .
```



## Features
### GUI
- **Code Loader and Inspector**: dynamically edit and load assembly code either from `.s` files or from `.o` ELF object files, disassembled in place.
- **Syntax Errors notice**: check for incorrect or unsupported instructions from the code text-box
- **Instruction Queue and Statistics**: inspect the current queue of instructions and their timings (issue time, execution steps and write-result time)
- **Register Inspector**: view and edit both integer and floating point registers in different formats (binary, decimal, hexadecimal)
- **Register Status Table**: inspect Tomasulo's register status table
- **Reservation Stations Table**: inspect the status of every Reservation Station's field: "cycles left to complete", "tag", "busy", "current instruction", and operands fields "Vj", "Vk", "Qj", "Qk", "A", and "Result"
- **Memory Dump**: live hexadecimal and ASCII dump of the memory

### Architecture
- **Tomasulo Algorithm**: a dynamic scheduling that allows the execution of multiple instructions using several execution units.
- **Multithreading**: Support for simulated multithreading

### Instruction Set Support
- 32 bits:
 - **RV32I**: base support for 32 bit integer operations
 - **RV32M**: 32 bit integer multiplication and division
 - **RV32F**: 32 bit floating point operations

### Other
- **Configurable**: a configuration window allows to tune many parameters
- **Sample Programs**: the `sample_programs` folder contains different ready to play with programs
- **Extensible**: adding support for more instruction sets is a matter of writing a JSON file



## Screenshots
...
