"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Tests/AnalysisPlotting.py

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


def test_plots():
    data = gen_fake_2pt_data()
    an = Analysis()
    an.init_resampler('Jackknife')
    corr = an.build_correlator(data)

    fit = an.fit([corr], ['cosh_2pt'], fit_ranges=[[15, 25]], correlation=False, args={'A': 1, 'E': 1},
           arg_identities=[['T', 'A', 'E']])

    plot = an.autoplot_fit(fit, overlays=['preliminary'], display_styles=['zoom:30,30'], fit_x_limits=[[15, 25]])
    plot.open()
    plot.close()
