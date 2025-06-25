# Amarino RV32
Minimal RISC-V processor with a 5 stage pipeline and compliant with the RV32I instruction set. Built entirely with [Amaranth HDL](https://github.com/amaranth-lang/amaranth) for the Arty A7 board.

## Build instructions
First, setup your Python environment

```bash
$ python -m venv .venv
$ . ./.venv/bin/activate
$ pip install amaranth yowasp-yosys
$ pip install git+https://github.com/amaranth-lang/amaranth-boards.git
$ export YOSYS=yowasp-yosys
$ export VIVADO=/path/to/vivado
```

To generate the bitstream and verilog code for the top-level module just run the `top.py` file as you would any python script.
