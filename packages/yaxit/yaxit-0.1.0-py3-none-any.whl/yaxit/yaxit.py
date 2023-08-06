
import xarray as xr
import pandas as pd
from .rest import open_remote
import os

class XarrayHistograms(xr.Dataset):
    __slots__ = ("pdf", "normed")

    @classmethod
    def from_rest_server(cls, url):
        
        return open_remote(url)

    def serve(self):
        serve_likelihood_inputs(self)

    def get_model(self, names=None, **roi):
        if isinstance(names, str):
            names = [names]
        if names is None:
            names = self.models.keys()
        indices = self.models.indexes
        binned = {k:slice(*v) for k,v in roi.items() if isinstance(indices[k], pd.IntervalIndex)}
        unbinned = {k:slice(*v) for k,v in roi.items() if k not in binned}
        data = self.models.copy()
        if unbinned:
            data = data.interp(**unbinned)
        if binned:
            data = data.sel(**binned)
        return data

    def add_model(self, model: xr.DataArray):
        self.models = xr.merge([self.models, model])
    
    def add_data(self, data: xr.DataArray):
        self.data = xr.merge([self.data, data])

    def to_binference(self, path):
        pass

    def to_xephyr(self, path):
        pass

    def to_zfit(self):
        pass

    def to_zarr(self, path):
        models_path = os.path.join(path, "yaxit_models.zarr")
        data_path = os.path.join(path, "yaxit_data.zarr")
        self.models.to_zarr(models_path)
        self.data.to_zarr(data_path)