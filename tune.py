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
    def __init__(self, rgb_array, crs, transform):
        super(Tune, self).__init__()
        self.rgb_array = rgb_array
        self.crs = crs
        self.transform = transform
        
    rgb_scalar = param.Number(1.0, bounds=(0.0, 10.0))
    red_scalar = param.Number(1.0, bounds=(0.0, 10.0))
    grn_scalar = param.Number(1.0, bounds=(0.0, 10.0))
    blu_scalar = param.Number(1.0, bounds=(0.0, 10.0))
    
    hist_kwargs = {
        'bins':50, 'histtype':'stepfilled', 'lw':0.0, 
        'stacked':False, 'alpha':0.3
    }

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
    
    def _adjust_array(self):
        '''
        '''
        arr = self.rgb_array * self.rgb_scalar
        red = arr[:,:,0] * self.red_scalar
        grn = arr[:,:,1] * self.grn_scalar
        blu = arr[:,:,2] * self.blu_scalar
        arr = np.dstack((red, grn, blu))

        return reshape_as_raster(arr)

    def _save_tiff(self, event):
        '''
        
        '''
        arr = self._adjust_array()

        logger.info('Writing .tif to disk...')

        with rasterio.open(
            'geotiffs/reference.tif',
            'w',
            driver='GTiff',
            height=arr.shape[1],
            width=arr.shape[2],
            count=3,
            dtype=arr.dtype,
            crs=self.crs,
            transform=self.transform,
        ) as dst:
            dst.write(arr[0,:,:], 1)
            dst.write(arr[1,:,:], 2)
            dst.write(arr[2,:,:], 3)

        logger.info('Write complete.')

    def instantiate_button(self):
        '''
        '''
        self.button = pn.widgets.Button(name='Save reference.tif to disk')
        self.button.on_click(self._save_tiff)
    
    @param.depends('rgb_scalar', 'red_scalar', 
                   'grn_scalar', 'blu_scalar')
    def serve_plots(self):
        '''
        '''
        arr = self._adjust_array()
        return self._plot_array(arr, self.hist_kwargs)
    
bands = ('red', 'grn', 'blu')
srcs = [rasterio.open(f"geotiffs/1_toa/center_{b}.tif") for b in bands]
downsampled_toa_bands = [s.read(1)[::50, ::50] for s in srcs]
rgb_array = np.dstack(tuple(downsampled_toa_bands))

tune = Tune(rgb_array=rgb_array, crs=srcs[0].crs, transform=srcs[0].transform)
tune.instantiate_button()

env = Environment(loader=FileSystemLoader('.'))
jinja_template = env.get_template('templates/tune.html')

tmpl = pn.Template(jinja_template)
tmpl.add_variable('app_title', '<h1>Histogram Reference Generator</h1>')
tmpl.add_panel('A', tune.serve_plots)
tmpl.add_panel('B', tune.param)
tmpl.add_panel('C', tune.button)

tmpl.servable()