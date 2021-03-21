''' Charles Stern '''
import os
import json
import requests
import logging

import rasterio
import numpy as np
import xarray as xr

import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

class Url():
    '''
    '''
    def __init__(self, base_url, latlon, datestring, suffixes):
        self.base_url = base_url
        self.latlon = latlon
        self.datestring = datestring
        self.suffixes = suffixes

    @staticmethod
    def _latlon2wrs(latlon):
        '''Translate latitude and longitude into WRS path and row.

        Parameters
        ----------
        latlon : 2-tuple
            latitude and longitude as floats
        
        Returns
        -------
        tuple
            WRS path and row as integers
        '''

        print("This function will transform latlon into wrs.")
        print("Input is %s", latlon)
        
        wrs = ('041', '036')
        print("Forcing specific values %s", wrs)

        return wrs

    def _assemble_scene_url(self):
        '''
        '''
        path, row = self._latlon2wrs(latlon=self.latlon)
        wrs_str = f'{path}/{row}'

        scene = f'LC08_L1TP_{path}{row}_{self.datestring}_01_T1'

        return f'{self.base_url}/{wrs_str}/{scene}/{scene}'

    def return_urls(self):
        '''
        '''
        scene_url = self._assemble_scene_url()
        return [scene_url + s for s in self.suffixes]

class Reflectance():
    '''

    '''
    @staticmethod
    def _load_scale_factors(filename, band_number):
        '''
        Parameters
        ----------

        Returns
        -------
        
        '''
        with open(filename) as f:
            metadata = json.load(f)
        M_p = metadata['L1_METADATA_FILE'] \
                    ['RADIOMETRIC_RESCALING'] \
                    ['REFLECTANCE_MULT_BAND_{}'.format(band_number)]
        A_p = metadata['L1_METADATA_FILE'] \
                    ['RADIOMETRIC_RESCALING'] \
                    ['REFLECTANCE_ADD_BAND_{}'.format(band_number)]
        return M_p, A_p
    
    def calc_reflectance(self, ds, band_number, metafile):
        '''
        Parameters
        ----------

        Returns
        -------
        
        '''
        M_p, A_p = self._load_scale_factors(metafile, band_number)
        toa = M_p * ds + A_p
        return np.squeeze(toa)


class Intake(Reflectance):
    '''Intakes data

    '''
    def __init__(self, urls):
        self.urls = urls

    @staticmethod
    def _download_file(in_filename, out_filename):
        '''
        Credit to Dask tutorial.
        '''
        if not os.path.exists(out_filename):
            print("Downloading", in_filename)
            response = requests.get(in_filename)
            with open(out_filename, 'wb') as f:
                f.write(response.content)

    def request_tiffs(self):
        '''
        '''
        raw_dir = config.paths["raw"]

        self.tiffs = [f'{raw_dir}/{k}.tiff' for k in config.bands.keys()]
        self.meta = f'{raw_dir}/meta.json'
        filenames = self.tiffs + [self.meta,]

        for url, fn in zip(self.urls, filenames):
            self._download_file(url, fn)

    def _return_toa_dict(self):
        '''
        Parameters
        ----------

        Returns
        -------
        
        '''
        chunks = {'band': 1, 'x': 1024, 'y': 1024}
        x_arrs = [xr.open_rasterio(t, chunks=chunks) for t in self.tiffs]

        toa_dict = {
            key:self.calc_reflectance(arr, band_number=i, metafile=self.meta)
            for arr, i, key in zip(x_arrs, (4,3,2), ('red', 'grn', 'blu')) 
        }
        return toa_dict

    @staticmethod
    def _write_gtiff(array, outpath, dims, crs, transform):
        '''
        Parameters
        ----------

        Returns
        -------
        
        '''
        with rasterio.open(
            outpath,
            'w',
            driver='GTiff',
            height=dims[0],
            width=dims[1],
            count=1,
            dtype=array.dtype,
            crs=crs,
            transform=transform,
        ) as dst:
            dst.write(array, 1)


    def save_toa_tiffs(self):
        '''Credit to the rasterio docs

        '''
        toa_dict = self._return_toa_dict()

        reference = rasterio.open(f'{config.paths["raw"]}/red.tiff')

        scene_id = 'center'
        print('This scene_id is temporary.')

        for i in range(len(toa_dict)):
            array = tuple(toa_dict.values())[i]
            band_name = tuple(toa_dict.keys())[i]
            self._write_gtiff(
                array=array,
                outpath=f'geotiffs/1_toa/{scene_id}_{band_name}.tif',
                dims=(array.shape[0], array.shape[1]),
                crs=reference.crs,
                transform=reference.transform,
            )
            print('Saved %s to disk', band_name)