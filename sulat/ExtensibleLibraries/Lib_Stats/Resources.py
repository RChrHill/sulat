"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/ExtensibleLibraries/Lib_Stats/Resources.py

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




class ResamplerBase:
    def resample(self, data):
        raise NotImplementedError

    def mean_definition(self, *args, **kwargs):
        raise NotImplementedError

    def submean_definition(self, *args, **kwargs):
        raise NotImplementedError

    def submean_double_definition(self, *args, **kwargs):
        raise NotImplementedError

    def cov_definition(self, submean, mean):
        raise NotImplementedError

    def cov_double_definition(self, submean, mean):
        raise NotImplementedError

    def var_definition(self, cov_definition):
        raise NotImplementedError

    def std_definition(self, var):
        raise NotImplementedError

    def covvarstd(self, mean, submean):
        cov = self.cov_definition(mean, submean)
        var = self.var_definition(cov)
        std = self.std_definition(var)

        return cov, var, std
