"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Core/Analysis/AnalysisBase.py

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

from sulat.Core.DataStructures import Correlator
from sulat.Core.DataStructures import Configurations


class AnalysisBase:
    def __init__(self):
        self.configurations = {}
        self.correlators = {}
        self.resampler = None

    def get_datastruct_lookup_parameters(self, name):
        pairs = [(self.configurations, Configurations),
                 (self.correlators, Correlator)]
        for typ, dct in pairs:
            if name in dct or issubclass(type(name), typ):
                search_dict = dct
                search_type = typ
                return search_dict, search_type
        raise ValueError(rf"Proposed data structure '{name}' is not in any internal database and is none of "
                         rf"{', '.join([elem[1].__name__ for elem in pairs])}")
