import os
import xarray, rioxarray

VRT_PATH = '/home/jovyan/datapod/sentinel2/urban_grammar_mosaic/composites/'

def build_year_mosaic(year, p=VRT_PATH):
    bands = []
    for b in [2, 3, 4]:
        band = (
            rioxarray.open_rasterio(
                os.path.join(p, f'{year}_B{b}.vrt'), chunks=True
            )
            .sel(band=1)
            .expand_dims(dim={'band': [b]})
        )
        bands.append(band)
    bands = xarray.concat(bands, dim='band')
    return bands

def build_multi_year(years):
    cube = []
    for y in years:
        year = (
            build_year_mosaic(y)
            .expand_dims(dim={'year': [y]})
        )
        cube.append(year)
    cube = xarray.concat(cube, dim='year')
    return cube