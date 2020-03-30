"""
Path hack to make tests work.
Avoid E402 module level import not at top of file)
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))