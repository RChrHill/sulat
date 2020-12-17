"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Core/Plotting/PlotConstructionKit/Utilities.py

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


def mk_default(kwarg_dict, key, value):
    if key not in kwarg_dict:
        kwarg_dict[key] = value


def errorband(fn, alpha, cov, args):
    """
    Based on code by Andreas Juettner.
    :param fn:
    :param alpha:
    :param cov:
    :param args:
    :return:
    """
    Df = np.zeros((len(alpha), len(args[0])))
    for i in range(len(alpha)):
        eps = np.zeros((len(alpha),))
        eps[i] = 0.01*alpha[i]
        dfp = fn(args[0], alpha+eps, *args[1:])
        dfm = fn(args[0], alpha-eps, *args[1:])
        if eps[i] == 0.:
            Df[i, :] = 0.
        else:
            Df[i, :] = 0.5*(dfp-dfm)/eps[i]
    df = 0

    if cov.shape == ():
        cov = [[cov]]
    for i in range(len(alpha)):
        for j in range(len(alpha)):
            df += Df[i, :]*Df[j, :]*cov[i][j]
    #df = np.sum(Df * np.dot(cov, Df), axis=0)  # Same as lines from df=0 onwards?

    return np.sqrt(df)

