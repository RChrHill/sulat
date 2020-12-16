"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/ExtensibleLibraries/Lib_FitFuncs/TwoPointFunctions.py

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


def exp_2pt(t, Zsq, energy):
    return (Zsq/(2*energy)) * np.exp(-energy * t)


def exp_2pt_excited(t, Aex0, Eex0, Aex1, Eex1):
    return exp_2pt(t, Aex0, Eex0) + exp_2pt(t, Aex1, Eex1)


def exp_2pt_series(t, *args):
    prefactors = args[::2]
    exponents = args[1::2]

    return sum([exp_2pt(t, prefactor, exponent) for prefactor, exponent in zip(prefactors, exponents)])


def cosh_2pt(t, T, Zsq, energy):
    return (Zsq/(2*energy)) * (np.exp(-energy * t) + np.exp(-energy * (T - t)))


def cosh_2pt_excited(t, T, Aex0, Eex0, Aex1, Eex1) -> float:

    return cosh_2pt(t, T, Aex0, Eex0) + cosh_2pt(t, T, Aex1, Eex1)


def corr_cosh_series(t, T, *args):
    prefactors = args[::2]
    exponents = args[1::2]

    return sum([cosh_2pt(t, T, prefactor, exponent) for prefactor, exponent in zip(prefactors, exponents)])
