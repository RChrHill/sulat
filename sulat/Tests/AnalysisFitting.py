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


def test_fit_twopoints():
    data = gen_fake_2pt_data()
    an = Analysis()
    an.init_resampler('Jackknife')
    corr = an.build_correlator(data)

    an.fit([corr], ['exp_2pt'], fit_ranges=[[15, 25]], correlation=True, args={'A': 1, 'E': 1},
           arg_identities=[['A', 'E']])
    an.fit([corr], ['exp_2pt_excited'], fit_ranges=[[3, 25]], correlation=True,
           args={'Aex0': 1, 'Eex0': 1, 'Aex1': 1, 'Eex1': 1},
           arg_identities=[['Aex0', 'Eex0', 'Aex1', 'Eex1']])

    an.fit([corr], ['cosh_2pt'], fit_ranges=[[15, 25]], correlation=True, args={'A': 1, 'E': 1},
           arg_identities=[['T', 'A', 'E']])
    an.fit([corr], ['cosh_2pt_excited'], fit_ranges=[[3, 25]], correlation=True,
           args={'Aex0': 1, 'Eex0': 1, 'Aex1': 1, 'Eex1': 1},
           arg_identities=[['T', 'Aex0', 'Eex0', 'Aex1', 'Eex1']])
