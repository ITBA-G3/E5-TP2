# Amarino RV32
Minimal RISC-V processor with a 5 stage pipeline and compliant with the RV32I instruction set. Built entirely with [Amaranth HDL](https://github.com/amaranth-lang/amaranth) for the [Arty A7](https://digilent.com/reference/programmable-logic/arty-a7/reference-manual?srsltid=AfmBOor-YDo2vV92jxzw3hyyqgcBs2t_OJYYgu6wmCi0nuK_S-leEfH4) board which features an Artix 7 from Xilinx.

## Build instructions
First, set up your Python environment

```bash
$ python -m venv .venv
$ . ./.venv/bin/activate
$ pip install amaranth yowasp-yosys
$ pip install git+https://github.com/amaranth-lang/amaranth-boards.git
$ export YOSYS=yowasp-yosys
$ export VIVADO=/path/to/vivado
```

To generate the bitstream and verilog code for the top-level module just run the `top.py` file as you would any python script.

## Find your way around the code
The top level module is in `top.py`. You'll find each module for the processor is in a seperate Python file and declared as a class inherting from `wiring.Component`. This is so that all interfaces between modules can be defined in `bus_signatures.py` and then connected explicitly in `top.py`. Everything runs on the Artix 7's default 100MHz clock. That is called automatically from the top level module since the `ArtyA7_100Platform` is set as the platform for building.

The `mvp-0` holds a more basic, single-stage implenentation.

Many modules and versions of the processor have their testbenches. These are ran in Amaranth's own simulator, although it would not be hard to automate them and create a more robust testing environment with PyTest and Cocotb. They all output `.vcd` files, some of which have a corresponding setup file for [Surfer](https://surfer-project.org/) which we strongly recommend as a waveform viewer since, among other great features, it can interpret signals as RV32 instructions.

## Exploring Block Diagrams
When you build the top module (or any module, for that matter) with the `do_build=True` option in Amaranth and the platform as any `XilinxPlatform` you'll find the Vivado project file (.xpr) in `build/`. You can open this in Vivado and run all the RTL, Synthesis, Timing Reports, etc... The schematic view is particularly interesing as it will show every connection before being optimized. You'll be able to see every module we coded in Amaranth as a block and then click on it to expand and see how the internal logic is made up.

Additionally, to get a better idea of how everything is connected you can look at the `top.v` file in the same folder. There should also be a `.il` file (if there isn't, it's easy to find in the Amaranth code for builing, you can just find the RTL step and write the `rtlil_text` contents to a text file). With this and `yowasp-yosys` you can generate the PostScript file that describes every connection found in the RTL step. It's better to do this in PostScript since the SVG mode onyl supports single modules. However, with GraphViz it's super easy to turn that PostScript code into an SVG file. Some helpful commands are [read_rtlil](https://yosyshq.readthedocs.io/projects/yosys/en/latest/cmd/read_rtlil.html) and [viz](https://yosyshq.readthedocs.io/projects/yosys/en/0.45/cmd/viz.html).
