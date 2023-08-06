

import itertools
import numpy as np
import xarray as xr
import pandas as pd
import pathlib
import h5py


def numpy_hist_to_xarray(hist, bins, dims=None, bin_decimals=7, **kwargs):
    if dims is None:
        dims = [f"dim_{i}" for i,_ in enumerate(bins)]
    bins = [np.around(b, bin_decimals) for b in bins]
    coords = {dim:pd.IntervalIndex.from_arrays(bs[:-1], bs[1:]) for dim,bs in zip(dims, bins)}
    extra = {}
    for dim, index in coords.items():
        extra[dim+"_center"] = (dim, index.mid)
    coords.update(**extra)
    coords.update(kwargs)
    return xr.DataArray(hist, dims=dims, coords=coords)

def multihist_to_xarray(histdd, dims=None,**kwargs):
    if dims is None:
        dims = histdd.axis_names
    return numpy_hist_to_xarray(histdd.histogram, histdd.bin_edges, dims, **kwargs)
    
def combine_xarray_histograms(plists, xarrays, **kwargs):
    plists = dict(plists)
    if len(plists):
        name, vs = plists.popitem()
        return xr.concat([combine_xarray_histograms(plists, xarrays, **dict({name:v}, **kwargs)) for v in vs], name)
    else:
        key = tuple(sorted(kwargs.items()))
        if key in xarrays:
            return xarrays[key]
        xarrays = {tuple(sorted(k)):v for k,v in xarrays.items()}
        if key in xarrays:
            return xarrays[key]
        else:
            raise ValueError(f"xarrays dict does not contain an xarray for {key}")
            
def read_templates(fdir, fname, histname, 
                  fparams={}, hist_params={},
                  hist_dims=None, multiplier=1., name=None):
    
    fdir = pathlib.Path(fdir)
    arrays = {}
    for fparam_vals in itertools.product(*fparams.values()):
        fkwargs = {k:v for k,v in zip(fparams, fparam_vals)}
        for v in fparam_vals:
            if isinstance(multiplier, dict):
                multiplier = multiplier.get(v)
            else:
                break
        path = fdir/fname.format(**fkwargs)
        bins = []
        axis_names = []
        with h5py.File(path, "r") as f:
            for k, b in f["bins"].items():
                bins.append(np.array(b))
                bn = b.attrs.get("name", f"axis_{k}")
                axis_names.append(bn)
            if hist_dims is None:
                dims = axis_names
            else:
                dims = hist_dims
            if len(dims) != len(bins):
                raise ValueError("The number of dimensions provided\
                     does not match the number of bin arrays in the file.")

            for param_vals in itertools.product(*hist_params.values()):
                kwargs = {k:v for k,v in zip(hist_params, param_vals)}
                kwargs.update(fkwargs)
                hist = np.array(f["templates/"+histname.format(**kwargs)])
                if multiplier is not None:
                    hist = hist*multiplier
                key = tuple(sorted(kwargs.items()))
                arrays[key] = numpy_hist_to_xarray(hist, bins, dims, **kwargs)

    combined = combine_xarray_histograms(dict(fparams, **hist_params), arrays)
    combined.attrs['filename'] = fname
    combined.attrs['histname'] = histname
    combined.attrs['filename_params'] = list(fparams)
    combined.attrs['histname_params'] = list(hist_params)
    if name is not None:
        combined.name = name
    return combined

def templates_from_specs(specs):
    models = xr.merge([read_templates(**model_spec) for model_spec in specs], compat='override')
    return models

def read_pandas(path, log10=True):
    df = pd.read_hdf(path, "table")
    df["r"] = df["r_3d_nn"]*df["r_3d_nn_egg"]
    # df = df[df["r"]<r2_max]
    if log10:
        df["cs2"] = np.log10(df["cs2_bottom"])
    return df

def read_data(fdir, fname, fparams={}, 
            dims=["cs1", "cs2", "r"],
            weight_name="counts", name=None,
            table_name="table",
            read_file=read_pandas):
    arrs = []
    for fparam_vals in itertools.product(*fparams.values()):
        fkwargs = {k:v for k,v in zip(fparams, fparam_vals)}
        fdir = pathlib.Path(fdir)
        path = fdir / fname.format(**fkwargs)
        df = read_file(path)
        coords = {dim: (weight_name, df[dim].values) for dim in dims}
        coords.update(**fkwargs)
        arr = xr.DataArray(np.ones(len(df)), coords=coords, dims=[weight_name])
        arrs.append(arr)
        
    arr = xr.concat(arrs, weight_name)
    if name is not None:
        arr.name = name
    return arr

