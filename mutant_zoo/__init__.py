# mutant_zoo/__init__.py

# Import the main classes/functions you want users to access directly
from .mutant_zoo import MutantZoo          # <-- the star of the show
from .design_round import DesignRound      # if this is a main class too
from .mutant import Mutant                 # if you have a Mutant class
from .utils import *                       # or selectively import what you want public

# Optional: define what gets imported with "from mutant_zoo import *"
# (most people disable star imports, but it's still nice to define)
__all__ = [
    "MutantZoo",
    "DesignRound",
    "Mutant",
    # add any functions/utils you want here
]

# Optional: set a nice package version (shows up in mutant_zoo.__version__)
__version__ = "0.1.0"