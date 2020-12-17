"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Tests/AnalysisCombo.py

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


def test_build_combination():
    data = gen_fake_2pt_data()
    an = Analysis()
    an.init_resampler('Jackknife')
    conf = an.build_configurations(data)
    an.configurations['conf'] = conf
    corr = an.build_correlator(data)
    an.correlators['corr'] = corr

    an.combine_configurations('{conf} + {conf}')
    an.combine('{conf} + {conf}')
    an.combine('flip', [conf])
    an.combine_correlators('{corr} + {corr}')
    an.combine('{corr} + {corr}')
    an.combine('flip', [corr])
