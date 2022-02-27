import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    from .analyzer import *
    from .app import *

except ModuleNotFoundError:
    print("Failed initializing sedimentanalyst - consider re-installation")
