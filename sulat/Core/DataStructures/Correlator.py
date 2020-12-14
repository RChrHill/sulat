"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Core/DataStructures/Correlator.py

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

from .ArithmeticMixIn import ArithmeticMixin
from sulat.Utilities.Evaluation import lazy_readonly

measurements = 0
variables = 1


class Correlator(ArithmeticMixin):
    """

    """
    ################
    # Constructors #
    ################
    def __init__(self, mean, submean, resampler):
        super().__init__()
        self._data_mean = mean
        self._submean = submean
        self.resampler = resampler

    ####################
    # Data description #
    ####################
    @property
    def data_mean(self):
        return self._data_mean

    @lazy_readonly
    def sample_mean(self):
        return np.mean(self._submean, axis=measurements)

    def forget_sample_mean(self):
        del self.sample_mean

    @property
    def submean(self):
        return self._submean

    ######################
    # Overridden Members #
    ######################
    @lazy_readonly
    def mean(self):
        return self.resampler.mean_definition(self._data_mean, self.sample_mean)

    @lazy_readonly
    def submean_double(self):
        return self.resampler.submean_double_definition(self._submean)

    @lazy_readonly
    def cov(self):
        return self.resampler.cov_definition(self.mean, self._submean)

    @lazy_readonly
    def cov_double(self):
        return self.resampler.cov_double_definition(self._submean, self.submean_double)

    @lazy_readonly
    def var(self):
        return self.resampler.var_definition(self.cov)

    @lazy_readonly
    def std(self):
        return self.resampler.std_definition(self.var)

    def forget_stats(self):
        del self.mean
        del self.submean_double
        del self.cov
        del self.cov_double
        del self.var
        del self.std

    ####################
    # Binary operators #
    ####################
    def _binop(self, op, other):
        cls = type(self)
        other_cls = type(other)
        if issubclass(other_cls, cls):
            mean = op(self._data_mean, other.data_mean)
            submean = op(self._submean, other.submean_definition)
        else:
            mean = op(self._data_mean, other)
            submean = op(self._submean, other)
        return cls(mean, submean, self.resampler)

    def _ibinop(self, op, other):
        cls = type(self)
        other_cls = type(other)
        if issubclass(other_cls, cls):
            self._data_mean = op(self._data_mean, other.data_mean)
            self._submean = op(self._submean, other.submean_definition)
        else:
            self._data_mean = op(self._data_mean, other)
            self._submean = op(self._submean, other)
        return self

    ##################
    # Unary Operator #
    ##################
    def _unop(self, op):
        self._data_mean = op(self._data_mean)
        self._submean = op(self._submean)
        self.forget_stats()
        return self
