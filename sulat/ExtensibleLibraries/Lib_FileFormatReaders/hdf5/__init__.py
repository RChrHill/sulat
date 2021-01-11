"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2021

File: sulat/ExtensibleLibraries/Lib_FileFormatReaders/hdf5/__init__.py

Author: Nils Asmussen <https://github.com/nils-asmussen>

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


import h5py
import numpy as np
import re
import glob
from .Resources import *

def hdf5(filepath, trajectory_fct='hadrons', filename_filter_fct=None, hdf5path=None, attributes=None):
    """Read HDF5 files.

    Keyword arguments:
        filepath -- path of the files to load with placeholders (e. g. '/path/corr_dt_*.*.h5')
        trajectory_fct -- Function taking filename and databasename as arguments and
                          returns a configuration number that is used to sort the data.
                          Data with trajectory 'None' is ignored.
                          (default: predefined function 'hadrons')
        filename_filter_fct -- Function taking the filename (full path) as argument and
                               returning a boolean whether to load the file.  (default: None)
        hdf5path -- regex string matching the full hdf5 path within the file (default: None)
        attributes -- attributes of the correlator or group containing the correlator
                      (e. g. {'gamma_snk':'Gamma5'}, default: None)
    """
    if isinstance(trajectory_fct, str):
        trajfct=load_hdf5_trajectory_fct_dict[trajectory_fct]
    else:
        trajfct=trajectory_fct
    if hdf5path is not None:
        hdf5pathregex=re.compile('^'+hdf5path+'$')
    else:
        hdf5pathregex=None
    data={}
    for filename in glob.iglob(filepath):
        if filename_filter_fct is None or filename_filter_fct(filename):
            with h5py.File(filename, 'r') as f:
                dsets=set()
                if hdf5path is not None \
                        and hdf5path in f \
                        and isinstance(f[hdf5path], h5py.Dataset):
                    dsets.add(f[hdf5path])
                else:
                    dsets=set()
                    _add_datasets(dsets, f)
                    dsets={ ds for ds in dsets if _dataset_filter(ds, hdf5pathregex, attributes) }
                for dset in dsets:
                    cfg=trajfct(filename, dset.name)
                    if cfg is not None:
                        assert cfg not in data, "Load HDF5: the configuration labeled "+str(cfg)+" already exists in data"
                        data[cfg]=_load_data(dset)
    trajs=list(data.keys())
    trajs.sort()
    result=np.concatenate([ data[traj] for traj in trajs ])
    T={ len(data[traj]) for traj in trajs }
    assert len(T)==1, 'Load HDF5: all data sets must have the same length (have '+str(T)+')'
    T=T.pop()
    return result.reshape(T, len(trajs), order='F')
