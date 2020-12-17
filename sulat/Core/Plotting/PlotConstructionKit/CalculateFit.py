"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Core/Plotting/PlotConstructionKit/CalculateFit.py

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
import numpy as np

from sulat.Core.Plotting.PlotConstructionKit.Utilities import errorband


def make_fit_centrals(x_range, subfit, ratio):
    candidate_data = subfit.fit_central(x_range)
    if ratio is not None:
        candidate_data = ratio(lambda x: subfit.fit_central(x), x_range)
    return candidate_data


def make_fit_error(x_range, subfit, ratio):
    if ratio is not None:
        def transformed_func(xs, argvals):
            return ratio(lambda x: subfit.fit(x, argvals), xs)
        fn = transformed_func
    else:
        fn = subfit.fit

    # Generate errors
    return errorband(fn=fn,
                     alpha=np.array(list(subfit.mean.values())),
                     cov=subfit.res_cov,
                     args=[x_range]
                     )


def make_fit_ydata(x_range, subfit, ratio):
    return make_fit_centrals(x_range, subfit, ratio), make_fit_error(x_range, subfit, ratio)
