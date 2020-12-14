"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Core/DataStructures/ArithmeticMixIn.py

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


import operator


class ArithmeticMixin:
    """

    """

    #####################
    # Binary Operations #
    #####################
    def _binop(self, op, other):
        raise NotImplementedError

    def _ibinop(self, op, other):
        raise NotImplementedError

    # Wouldn't it be wonderful to define these in a for loop...
    def __add__(self, other):
        return self._binop(operator.add, other)

    def __iadd__(self, other):
        return self._ibinop(operator.iadd, other)

    def __sub__(self, other):
        return self._binop(operator.sub, other)

    def __isub__(self, other):
        return self._ibinop(operator.isub, other)

    def __mul__(self, other):
        return self._binop(operator.mul, other)

    def __imul__(self, other):
        return self._ibinop(operator.imul, other)

    def __truediv__(self, other):
        return self._binop(operator.truediv, other)

    def __itruediv__(self, other):
        return self._ibinop(operator.itruediv, other)

    def __floordiv__(self, other):
        return self._binop(operator.floordiv, other)

    def __ifloordiv__(self, other):
        return self._ibinop(operator.ifloordiv, other)

    def __mod__(self, other):
        return self._binop(operator.mod, other)

    def __imod__(self, other):
        return self._binop(operator.imod, other)

    def __pow__(self, other):
        return self._binop(operator.pow, other)

    def __ipow__(self, other):
        return self._ibinop(operator.ipow, other)

    def __lshift__(self, other):
        return self._binop(operator.lshift, other)

    def __ilshift__(self, other):
        return self._ibinop(operator.ilshift, other)

    def __rshift__(self, other):
        return self._binop(operator.rshift, other)

    def __irshift__(self, other):
        return self._ibinop(operator.irshift, other)

    def __and__(self, other):
        return self._binop(operator.and_, other)

    def __iand__(self, other):
        return self._ibinop(operator.iand, other)

    def __or__(self, other):
        return self._binop(operator.or_, other)

    def __ior__(self, other):
        return self._ibinop(operator.ior, other)

    def __xor__(self, other):
        return self._binop(operator.xor, other)

    def __ixor__(self, other):
        return self._ibinop(operator.ixor, other)

    ####################
    # Unary Operations #
    ####################
    def _unop(self, op):
        raise NotImplementedError

    def __neg__(self):
        return self._unop(operator.neg)

    def __pos__(self):
        return self._unop(operator.pos)

    def __abs__(self):
        return self._unop(operator.abs)

    def __invert__(self):
        return self._unop(operator.invert)
