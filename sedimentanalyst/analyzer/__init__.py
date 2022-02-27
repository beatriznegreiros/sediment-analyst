import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    from .static_plotter import *
    from .statistical_analyzer import *
    from .utils import *

except ModuleNotFoundError:
    print("Failed initializing Module analyzer - consider re-installation")
