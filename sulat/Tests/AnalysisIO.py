"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Tests/AnalysisIO.py

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

from sulat import Analysis
from .Utilities import gen_fake_2pt_data


def test_build_configurations():
    data = gen_fake_2pt_data()
    an = Analysis()
    an.build_configurations(data)
    an.build_configurations(data, transforms={'roll': [10, 0]})
    an.build_configurations(data, transforms={'roll': [10, 0]})
    an.build_configurations(data, transforms={'roll_timeslices': [10]})
    an.build_configurations(data, transforms={'roll_configurations': [10]})
    an.build_configurations(data, transforms=['fold'])
    an.build_configurations(data, transforms={'fold': [1, 0]})
    an.build_configurations(data, transforms={'fold': [10, 0]})
    an.build_configurations(data, transforms={'fold': [10, 10]})
    an.build_configurations(data, transforms=['flip'])
    an.build_configurations(data, transforms={'bin': [2, 0]})
    an.build_configurations(data, transforms={'bin': [2, 1]})
    an.build_configurations(data, transforms={'bin_timeslices': [2]})
    an.build_configurations(data, transforms={'bin_configurations': [2]})
