"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2020

File: sulat/Core/Fitting/JointCovariance.py

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

measurements = 0
timeslices = 1


def joint_weights_matrix(correlators, fit_ranges, correlation, frozen):
    central_cov, subcovs = joint_cov(correlators, fit_ranges, correlation, frozen)
    central_weights = cov2weights(central_cov)
    # It's a bit messy to have two if statements operating on the 'frozen' argument, but it allows us to both increase
    # atomicity and make a CPU+memory saving in the frozen case
    if frozen:
        return central_weights, [central_weights for _ in subcovs]
    else:
        return central_weights, [cov2weights(subcov) for subcov in subcovs]


def joint_cov(correlators, fit_ranges, correlation, frozen):
    means = np.concatenate([corr.mean for corr in correlators], axis=0)
    submeans = np.concatenate([corr.submean for corr in correlators], axis=timeslices)

    assert all([isinstance(corr.resampler, type(correlators[0].resampler)) for corr in correlators]), \
           "Input correlators do not all have the same resampling method."

    cov_func = correlators[0].resampler.cov_definition
    double_cov_func = correlators[0].resampler.cov_double_definition
    C, T = correlators[0].submean.shape

    total_cov = cov_func(means, submeans)
    central_cov = cutdown_and_correlate(total_cov, fit_ranges, correlation, T)

    if frozen:
        return central_cov, [central_cov for _ in range(C)]
    else:
        double_submeans = np.concatenate([corr.submean_double for corr in correlators], axis=timeslices+1)
        cov_double = double_cov_func(submeans, double_submeans)
        sub_covs = []
        for subtotal_cov in cov_double:
            sub_cov = cutdown_and_correlate(subtotal_cov, fit_ranges, correlation, T)
            sub_covs.append(sub_cov)
        return central_cov, sub_covs


def cov2weights(cov):
    return np.linalg.cholesky(np.linalg.inv(cov))


def cutdown_and_correlate(total_cov, fit_ranges, correlation, T):
    all_blocks = []
    for i, fr1 in zip(range(len(fit_ranges)), fit_ranges):
        rowblocks = []
        for j, fr2 in zip(range(len(fit_ranges)), fit_ranges):
            covblock = total_cov[i*T:(i+1)*T, j*T:(j+1)*T]
            val = covblock[fr1][:, fr2]
            if correlation == 'block' and i != j:
                val[:, :] = 0
            rowblocks.append(val)
        all_blocks.append(np.hstack(rowblocks))
    cov = np.vstack(all_blocks)

    if not correlation:
        cov = np.diag(np.diag(cov))

    return cov
