"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/ExtensibleLibraries/Lib_Minimisers/LevenburgMarquardtScipy/Resources.py

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

from sulat.ExtensibleLibraries.Lib_Minimisers.Resources import p_value


def mk_sqresiduals(args, vec_data, sqCinv, funcs, xs, parameter_maps, fit_parameter_slots):
    """
    Computes the square residuals between a fitted function and some data.
    """
    fit_data = np.concatenate([func(x, args, p_map, p_slot) for func, x, p_map, p_slot in zip(funcs, xs, parameter_maps, fit_parameter_slots)])

    err = np.array(np.dot(vec_data - fit_data, sqCinv))
    return err


def mkchisqval(res):
    """
     takes result of scipy.opt.leastsq as input and returns
         p-value,
         chi^2/Ndof
         Ndof
    """
    Ndof = len(res[2]['fvec']) - len(res[0])
    chisq = sum(res[2]['fvec'] ** 2.0)
    pv = p_value(Ndof, chisq)
    return pv, chisq / Ndof, Ndof
