"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/ExtensibleLibraries/Lib_Minimisers/LevenburgMarquardtScipy/__init__.py

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
import scipy.optimize as opt

from .Resources import mk_sqresiduals, mkchisqval


def LevenburgMarquardtScipy(vd, args, sqCinv, funcs, xs, parameter_maps, fit_parameter_slots):
    """
    Fits a function to some input data using the Levenburg-Marquardt algorithm supplied by scipy.optimize.leastsq.
    :param vd:
    :param args:
    :param sqCinv:
    :param funcs:
    :param xs:
    :param parameter_maps:
    :param fit_parameter_slots:
    :return:
    """
    # function wrapper in rescos.
    res = opt.leastsq(mk_sqresiduals, args, args=(vd, sqCinv, funcs, xs, parameter_maps, fit_parameter_slots), maxfev=2000, ftol=1e-10, xtol=1e-10, full_output=True)
    # get chisquared value
    fit_statistics = mkchisqval(res)
    # extract data from the fitting
    parameters = np.zeros(len(args))
    for ii in range(0, len(args)):
        parameters[ii] = res[0][ii]

    return parameters, fit_statistics, res[2]['fvec']
