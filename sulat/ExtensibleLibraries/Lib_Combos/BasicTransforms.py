"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/ExtensibleLibraries/Lib_Combos/BasicTransforms.py

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

configurations = 0
timeslices = 1


def roll(data, shift, axis):
    """
    Wrapper function for numpy.roll. See the numpy documentation for full information.

    :param data: A numpy array.
    :param shift: The number of variables to shift by.
    :param axis: The axis to roll over.
    :return:
    """
    return np.roll(data, shift, axis=axis)


def roll_timeslices(data, shift):
    """
    Wrapper function for numpy.roll. See the numpy documentation for full information. Locked to the 'timeslices' axis.

    :param data: A numpy array.
    :param shift: The number of variables to shift by.
    :return:
    """
    return roll(data, shift, timeslices)


def roll_configurations(data, shift):
    """
    Wrapper function for numpy.roll. See the numpy documentation for full information. Locked to the 'configurations' axis.

    :param data: A numpy array.
    :param shift: The number of variables to shift by.
    :return:
    """
    return roll(data, shift, configurations)


def fold(data, cutoff=1, backshift=0):
    """
    Returns the average of a slice of a numpy array and the time-reversed slice. By default, the slice cuts off the first timeslice of the array.
    Based on code by Jonathan Flynn.

    :param data: A numpy array.
    :param cutoff: The number of initial timeslices to ignore.
    :param backshift: The number of timeslices to shift the slice back by.
    :return:
    """
    lo = cutoff - backshift
    hi = data.shape[timeslices]-backshift
    assert cutoff >= backshift, f"Backshift {backshift} is larger than the cutoff {cutoff}."
    data[:, lo:hi] = 0.5 * (data[:, lo:hi] + data[:, lo:hi][:, ::-1])
    return data


def flip(data):
    """
    Reverses the input numpy array along the timeslices-axis.
    :param data: A numpy array.
    :return:
    """
    return np.flip(data, axis=timeslices)


def bin(data, binsize, axis):
    """
    Averages consecutive values of a numpy array.

    :param data: A numpy array.
    :param binsize: The number of values to include in each bin.
    :param axis: The axis to bin over.
    :return:
    """
    length = data.shape[axis]
    staxis = axis + 1
    # TODO: implement C%binsize!=0 case
    assert length % binsize == 0, f'Binsize {binsize} not an integer divisor of shape along axis {axis}: {length}.'
    num_bins = length // binsize
    return np.mean(np.stack(np.split(data, num_bins, axis=axis), axis=axis), axis=staxis)


def bin_configurations(data, binsize):
    """
    Averages 'binsize' consecutive configurations.

    :param data: A numpy array.
    :param binsize: The number of configurations to include in each bin.
    :return:
    """
    return bin(data, binsize, configurations)


def bin_timeslices(data, binsize):
    """
    Averages 'binsize' consecutive timeslices.

    :param data: A numpy array.
    :param binsize: The number of timeslices to include in each bin.
    :return:
    """
    return bin(data, binsize, timeslices)
