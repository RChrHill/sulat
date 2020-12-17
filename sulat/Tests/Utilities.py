"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Tests/Utilities.py

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


def gen_fake_2pt_data():
    rng = np.random.default_rng(10)

    t, c, amp, energy, energy_2 = 64, 50, 0.03, 0.08, 0.8
    random_generated_numbers = rng.normal(scale=0.01, size=(t, c))
    lin_data = np.outer(amp * (np.exp(-energy * np.arange(t)) + np.exp(-energy * (t - np.arange(t)))),
                        np.ones(c)) + np.outer(
        amp * (np.exp(-energy_2 * np.arange(t)) + np.exp(-energy_2 * (t - np.arange(t)))), np.ones(c))
    data = lin_data + lin_data * random_generated_numbers

    return data
