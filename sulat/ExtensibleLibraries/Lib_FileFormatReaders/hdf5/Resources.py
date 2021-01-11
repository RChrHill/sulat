"""
sulat data analysis library for Lattice QCD (available at: https://github.com/RChrHill/sulat)

Copyright (C) 2018-2021

File: sulat/ExtensibleLibraries/Lib_FileFormatReaders/hdf5/Resources.py

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

def load_hdf5_trajectory_fct_hadrons(filename, datasetname):
    have_dt=filename.find('_dt_')!=-1
    parts=filename.split('.')
    if len(parts)<3 or parts[-1]!='h5':
        return None # ignore the file
    traj=int(parts[-2])
    if have_dt:
        parts=parts[-3].split('_dt_')
        dt=int(parts[-1])
        traj=traj*10000+dt
    return traj

load_hdf5_trajectory_fct_dict={
        'hadrons':load_hdf5_trajectory_fct_hadrons,
        }

def _compare_hdf5_attribute(attrib, val):
    v={ False:[val], True:val }[isinstance(val, list)]
    if len(attrib) != len(v):
        return False
    for xi, y in zip(attrib,v):
        if hasattr(xi, 'decode'): #handle byte strings
            x=xi.decode()
        else:
            x=xi
        if x != y:
            return False
    return True

def _add_datasets(dsets, h5pygroup):
    for i in h5pygroup.values():
        if isinstance(i, h5py.Group):
            _add_datasets(dsets, i)
        elif isinstance(i, h5py.Dataset):
            dsets.add(i)

def _dataset_filter(dataset, hdf5pathregex, attributes):
    if hdf5pathregex is not None and not hdf5pathregex.match(dataset.name):
        return False
    if attributes is not None:
        group=dataset.parent
        gattrs=group.attrs
        dattrs=dataset.attrs
        for key, val in attributes.items():
            if          ( key not in dattrs or not _compare_hdf5_attribute( dattrs[key], val ) ) \
                    and ( key not in gattrs or not _compare_hdf5_attribute( gattrs[key], val ) ):
                return False
    return True

def _load_data(dataset):
    if dataset.dtype.names == ('re', 'im'):
        return dataset['re']+1j*dataset['im']
    assert False, "Load HDF5: loading dataset of type "+str(dataset.dtype)+" not implemented"
