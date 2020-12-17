"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/ExtensibleLibraries/Lib_PlotOverlays/InfoDisplay.py

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


def goodness_of_fit(ax, *args):
    fit = args[0]
    ax.text(0.99, .35, 'P value: ' + str(round(fit.pvalue, 3)), horizontalalignment='right', transform=ax.transAxes)
    ax.text(0.99, .29, '$\chi^2$/DOF: ' + str(round(fit.chi_sq_per_dof, 3)), horizontalalignment='right', transform=ax.transAxes)
    ax.text(0.99, .24, '# DOF: ' + str(int(round(fit.N_dof, 0))), horizontalalignment='right', transform=ax.transAxes)


def preliminary(ax, *args):
    ax.text(0.05, 0.75, "PRELIMINARY", fontsize=48, rotation=30, transform=ax.transAxes, color='black', alpha=0.1)
