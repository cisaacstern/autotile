import logging

import numpy as np
import param
import panel as pn
import rasterio
from rasterio.plot import (
    show as rshow,
    show_hist as rshow_hist,
    reshape_as_raster, 
    reshape_as_image,
)
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Tune(param.Parameterized):
    '''
    '''
    def __init__(self, sources):
        super(Tune, self).__init__()
        self.sources = sources
        self.crs = sources[0].crs
        self.transform = sources[0].transform
        self.lowres_arr = self._resample(stride=50)
        self.fullres_arr = self._resample(stride=None)
        
    rgb_scalar = param.Number(1.0, bounds=(0.0, 10.0))
    red_scalar = param.Number(1.0, bounds=(0.0, 10.0))
    grn_scalar = param.Number(1.0, bounds=(0.0, 10.0))
    blu_scalar = param.Number(1.0, bounds=(0.0, 10.0))
    
    hist_kwargs = {
        'bins':50, 'histtype':'stepfilled', 'lw':0.0, 
        'stacked':False, 'alpha':0.3
    }

    def _resample(self, stride):
        '''

        '''
        sampled_bands = [s.read(1)[::stride, ::stride] for s in self.sources]
        return np.dstack(tuple(sampled_bands))

    @staticmethod
    def _plot_array(array, hist_kwargs):
        '''
        '''
        fig, axs = plt.subplots(1, 2, figsize=(14,7))
        rshow(array, ax=axs[0])
        rshow_hist(array, **hist_kwargs, ax=axs[1])
        axs[1].set_xlim(0,1)
        axs[1].set_ylim(0,3000)
        plt.close('all')
        return fig
    
    def _adjust_array(self, arr):
        '''
        '''
        arr = arr * self.rgb_scalar
        red = arr[:,:,0] * self.red_scalar
        grn = arr[:,:,1] * self.grn_scalar
        blu = arr[:,:,2] * self.blu_scalar
        arr = np.dstack((red, grn, blu))

        return reshape_as_raster(arr)

    @staticmethod
    def _write_tiff(arr, outpath, crs, transform):
        '''
        
        '''
        logger.info('Writing %s to disk...', outpath)

        with rasterio.open(
            outpath,
            'w',
            driver='GTiff',
            height=arr.shape[0],
            width=arr.shape[1],
            count=1,
            dtype=arr.dtype,
            crs=crs,
            transform=transform,
        ) as dst:
            dst.write(arr, 1)

        logger.info('Write complete.')

    
    def _save_on_click(self, event):
        '''
        
        '''
        arr = self._adjust_array(arr=self.fullres_arr)
        for i, band in zip(range(3), ('red','grn','blu')):
            self._write_tiff(
                arr[i,:,:],
                outpath=f'geotiffs/2_hst/center_{band}.tif',
                crs=self.crs,
                transform=self.transform,
            )
            print('Saved following band to geotiffs/2_hst/...', band)

    def instantiate_button(self):
        '''
        '''
        self.button = pn.widgets.Button(name='Save hist-adjusted tifs to disk')
        self.button.on_click(self._save_on_click)
    
    @param.depends('rgb_scalar', 'red_scalar', 'grn_scalar', 'blu_scalar')
    def serve_plots(self):
        '''
        '''
        arr = self._adjust_array(arr=self.lowres_arr)
        return self._plot_array(arr, self.hist_kwargs)
    
bands = ('red', 'grn', 'blu')
sources = [rasterio.open(f"geotiffs/1_toa/center_{b}.tif") for b in bands]

tune = Tune(sources=sources)
tune.instantiate_button()

env = Environment(loader=FileSystemLoader('.'))
jinja_template = env.get_template('templates/tune.html')

tmpl = pn.Template(jinja_template)
tmpl.add_variable('app_title', '<h1>Histogram Reference Generator</h1>')
tmpl.add_panel('A', tune.serve_plots)
tmpl.add_panel('B', tune.param)
tmpl.add_panel('C', tune.button)

tmpl.servable()