import sys
import os
# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))
    
# Construct the path to the folder containing the file to import
folder_path = os.path.join(current_dir, '..') # Go up

# Add the folder to the Python path
sys.path.append(folder_path)

from Register_Bank.regbank import RegBank
from ALU.alu import ALU
from amaranth import *

