import pathlib

bands = {
    'red' : '_B4.TIF',
    'grn' : '_B3.TIF',
    'blu' : '_B2.TIF',
}

url_args = {
    'base_url': 'https://landsat-pds.s3.amazonaws.com/c1/L8', 
    'latlon': ('a', 'b'), 
    'datestring': '20141108_20170303', 
    'suffixes': list(bands.values()) + ['_MTL.json',],
}

paths = {
    target : pathlib.Path('geotiffs', f'{i}_{target}')
    for i, target in enumerate(('raw','toa','hst','cog'))
}
