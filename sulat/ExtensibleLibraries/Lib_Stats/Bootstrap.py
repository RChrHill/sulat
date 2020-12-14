"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/ExtensibleLibraries/Lib_Stats/Bootstrap.py

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
from sulat.Utilities.Evaluation import lazy_readonly


class Bootstrap(ResamplerBase):
    def __init__(self, seed, nsamples):
        self.rng = np.random.default_rng(seed)
        self.nsamples = nsamples
        self.configs = None

    @lazy_readonly
    def random_numbers(self):
        return self.rng.integers(0, self.configs, size=(self.configs, self.nsamples))

    def resample(self, data):
        configs = data.shape[0]
        if self.configs is None:
            self.configs = configs
        if configs != self.random_numbers.shape[0]:
            raise ValueError(f"Bootstrap was initialised for {self.configs} configurations, not {configs}. Please re-initialise the resampler with `Analysis.configure_resampler'.")
        return np.mean(data[self.random_numbers], axis=0)

    def configure(self, seed=None, nsamples=None):
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        if nsamples is not None:
            self.nsamples = nsamples
        del self.random_numbers

    #######################
    # Used by Correlators #
    #######################
    def mean_definition(self, data_mean, sample_mean):
        return data_mean

    def cov_definition(self, mean, submean):
        submean = np.atleast_2d(submean)
        mean = np.atleast_1d(mean)
        num_configs = submean.shape[-1]
        d = (submean - mean[None, :])
        return np.dot(d.T, d)/num_configs

    def var_definition(self, cov):
        return np.diag(np.atleast_2d(cov))

    def std_definition(self, var):
        return np.sqrt(var)
