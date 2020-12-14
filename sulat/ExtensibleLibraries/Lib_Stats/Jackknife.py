"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/ExtensibleLibraries/Lib_Stats/Jackknife.py

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

from .Resources import ResamplerBase

configurations = 0
timeslices = 1


class Jackknife(ResamplerBase):

    def resample(self, data):
        mn = np.sum(data, axis=configurations)
        w = (mn[None, :] - data)/(data.shape[configurations] - 1)
        return w

    #######################
    # Used by Correlators #
    #######################
    def mean_definition(self, data_mean, sample_mean):
        return sample_mean

    def submean_double_definition(self, submean):
        num_samples = submean.shape[configurations]
        # Add get total value for each x-value
        mn = np.sum(submean, axis=configurations)
        # Make all double-removals
        jackknife_removed_data = submean[None, :, :] + submean[:, None, :]
        # Drop the diagonal in the configs x configs slice --- same value removed twice instead of different values
        new_shape = list(jackknife_removed_data.shape)
        new_shape[configurations + 1] -= 1
        jackknife_removed_data = jackknife_removed_data[~np.eye(num_samples, dtype=bool), :].reshape(*new_shape)

        # Subtract double-removal from each total, divide to make the average over the N-2 samples
        sub_double = (mn[None, None, :] - jackknife_removed_data) / (submean.shape[configurations] - 2)
        return sub_double

    def cov_definition(self, mean, submean):
        submean = np.atleast_2d(submean)
        mean = np.atleast_1d(mean)
        num_configs = submean.shape[configurations]
        d = (submean - mean[None, :])
        return np.dot(d.T, d)*((num_configs - 1)/num_configs)

    def cov_double_definition(self, submean, submean_double):
        submean_double = np.atleast_3d(submean_double)
        data = np.atleast_2d(submean)
        num_configs = submean.shape[configurations]
        d = submean_double - data[:, None, :]
        return np.matmul(d.swapaxes(1, 2), d)*((num_configs - 1)/num_configs)

    def var_definition(self, cov):
        return np.diag(cov)

    def std_definition(self, var):
        return np.sqrt(var)
