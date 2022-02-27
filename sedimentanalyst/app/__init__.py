import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    from .interac_plotter import *
    from .web_application import *

except ModuleNotFoundError:
    print("Failed initializing App - consider re-installation")