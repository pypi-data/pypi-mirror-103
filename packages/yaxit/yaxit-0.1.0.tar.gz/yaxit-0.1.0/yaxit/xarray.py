import xarray as xr
import pandas as pd
import numpy as np


class XarrayInterface:
    def __init__(self, obj):
        self._obj = obj

    def as_sampled(self):
        obj = self._obj.copy()
        for dim, index in obj.indexes.items():
            if isinstance(index, pd.IntervalIndex):
                obj.coords[f"{dim}__left"] = (dim, index.left)
                obj.coords[f"{dim}__right"] = (dim, index.right)
                obj.coords[dim] = index.mid
        return obj

    def as_binned(self):
        obj = self._obj.copy()
        for dim in obj.dims:
            lname,rname = dim+"__left", dim+"__right"
            if lname in obj and rname in obj:
                bls, brs = obj[lname], obj[rname]
                obj.coords[dim] = (dim, pd.IntervalIndex.from_arrays(bls, brs))
                obj = obj.drop([lname,rname])
        return obj

    def is_binned(self, dim=None):
        if dim is None:
            return bool(self.binned_dims)
        return (isinstance(self._obj.indexes[dim], pd.IntervalIndex) 
                or (dim+"__left" in self._obj and dim+"__right" in self._obj))

    @property
    def binned_dims(self):
        return [dim for dim in self._obj.dims if self.is_binned(dim)]
    
    @property
    def bin_widths(self):
        obj = self.as_binned()
        bins = {}
        for dim, index in obj.indexes.items():
            if isinstance(index, pd.IntervalIndex):
                bins[dim] = index.length.values
        return bins

    @property
    def bin_volumes(self):
        obj = self.as_binned()
        bins = obj.yaxit.bin_widths
        volumes = xr.DataArray(np.product(np.meshgrid(*[bins[dim] for dim in bins], indexing="ij"), axis=0),
                              coords={dim: (dim, self._obj.coords[dim]) for dim in bins}, dims=list(bins),
                              )
        return volumes

    @property
    def density(self):
        return self._obj/self.bin_volumes

    @property
    def mus(self):
        return self._obj.sum(self.binned_dims)

    @property
    def pdf(self):
        return self.density/self.mus

    def to_zarr(self, *args, **kwargs):
        obj = self.as_sampled()
        return obj.to_zarr(*args, **kwargs)

@xr.register_dataset_accessor("yaxit")
class DatasetInterface(XarrayInterface):

    def serve(self, *args, **kwargs):
        import xpublish
        obj = self.as_sampled()
        obj.rest.serve(*args, **kwargs)
    
    def Dashboard(self, *args, **kwargs):
        from xrviz.dashboard import Dashboard
        obj = self._obj
        if self.is_binned:
            obj = self.as_sampled()
        return Dashboard(obj, *args, **kwargs)

@xr.register_dataarray_accessor("yaxit")
class ArrayInterface(XarrayInterface):
    pass
