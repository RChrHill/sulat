"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Core/DataStructures/Configurations.py

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
import copy

from .ArithmeticMixIn import ArithmeticMixin
from sulat.Utilities.Evaluation import lazy_readonly


measurements = 0
variables = 1


class Configurations(ArithmeticMixin):
    """

    """
    def __init__(self, data):
        super().__init__()
        self._data = copy.deepcopy(data)

    @lazy_readonly
    def mean(self):
        return np.mean(self._data, axis=measurements)

    @property
    def data(self):
        return self._data

    def forget_stats(self):
        del self.mean

    #############
    # Operators #
    #############
    def _unop(self, op):
        self._data = op(self._data)
        self.forget_stats()
        return self

    # Note: The if/else statements here add 100-200ns overhead to each call
    # Another 100-200ns gets added by the encapsulation via _binop and _ibinop
    ####################
    # Binary operators #
    ####################
    def _binop(self, op, other):
        cls = type(self)
        other_cls = type(other)
        if issubclass(other_cls, cls):
            data = op(self._data, other.data)
        else:
            data = op(self._data, other)
        return cls(data)

    def _ibinop(self, op, other):
        cls = type(self)
        other_cls = type(other)
        if issubclass(other_cls, cls):
            self._data = op(self._data, other.data)
        else:
            self._data = op(self._data, other)
        return self
