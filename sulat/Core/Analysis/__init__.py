"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Core/Analysis/__init__.py

Author: Nils Asmussen <https://github.com/nils-asmussen>
Author: Ryan Hill <https://github.com/RChrHill>
Author: James Richings <https://github.com/JPRichings>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from .Combo import MixInCombo
from .IO import MixInDataIO
from sulat.Utilities.ExLibFunction import ExLibFunction
from sulat.ExtensibleLibraries.Lib_Stats import ExLib_Stats


def get_resampler_initialiser(Exlib, args):
    """
    Pass the name of the resampler to use.
    Additional arguments to the init_resampler function are passed to the initialiser of the resampler class.
    """
    return Exlib.lookup(args)


class Analysis(MixInCombo, MixInDataIO):
    @ExLibFunction(resampler=(ExLib_Stats, get_resampler_initialiser))
    def init_resampler(self, resampler, *args, **kwargs):
        self.resampler = resampler(*args, **kwargs)

    def configure_resampler(self, *args, **kwargs):
        self.resampler.configure(*args, **kwargs)
