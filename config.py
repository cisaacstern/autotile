import pathlib

bands = {
    'red' : '_B4.TIF',
    'grn' : '_B3.TIF',
    'blu' : '_B2.TIF',
}

url_args = {
    'base_url': 'https://landsat-pds.s3.amazonaws.com/c1/L8', 
    'datestring': '20141108_20170303', 
    'suffixes': list(bands.values()) + ['_MTL.json',],
}

paths = {
    target : pathlib.Path('geotiffs', f'{i}_{target}')
    for i, target in enumerate(('raw','toa','hst','cog'))
}

tiles_url_tail = '/rgb/{z}/{x}/{y}.png?r=red&g=grn&b=blu&r_range=[0,1]&g_range=[0,1]&b_range=[0,1]'

tiles = {
    'hst' : {
        'name' : 'Histogram-matched COGs',
        'tiles' : 'http://localhost:5001' + tiles_url_tail,
    },
    'toa' : {
        'name' : 'Top-of-atmosphere COGs',
        'tiles' : 'http://localhost:5000' + tiles_url_tail, 
    }
}