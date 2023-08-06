import xarray as xr

import yaxit.xarray

def open_remote(url):
    import zarr
    from fsspec.implementations.http import HTTPFileSystem
    fs = HTTPFileSystem()
    mapper = fs.get_mapper(url)
    ds = xr.open_zarr(mapper, consolidated=True).yaxit.as_binned()
    return ds