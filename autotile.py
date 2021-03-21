import sys
import subprocess
import logging

from jinja2 import Environment, FileSystemLoader

import config
import intake

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AutoTile(intake.Intake):

    def __init__(self, location, tooltip, tiles, **kwargs):
        super(AutoTile, self).__init__(**kwargs)
        self.location = location
        self.tooltip = tooltip
        self.tiles = tiles

    def write_toa_tiffs(self):
        '''
        '''
        self.request_tiffs()
        self.save_toa_tiffs()

    def render_streamlit_view(self):
        '''
        '''
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('templates/view.py')

        rendered_view = template.render(
            tooltip=self.tooltip,
            location=self.location,
        )

        with open("_rendered_view.py", "w") as dst:
            dst.write(rendered_view)

class OptimizedIngest():
    
    def optimize_tiffs_as_cogs(self):
        '''
        '''
        subprocess.run(["./scripts/optimize.sh"])

    def ingest_cogs_to_sqlite(self, scene_id):
        '''
        '''
        for path, database in zip(
            ('$NOT_MATCHED/', '$MATCHED/'),
            ('_notmatched.sqlite', '_matched.sqlite')):

            filepattern = f'{path}' + scene_id + "_{band}.tif"
            cmd = f"terracotta ingest {filepattern} -o {database}"
            subprocess.Popen(cmd, shell=True)

    
if __name__ == '__main__':

    if sys.argv[1] == 'help':

        print("""
        Start with, e.g.:
            autotile stage 34.0739 -118.2400 'Dodger Stadium'
        """)
    
    elif sys.argv[1] == 'stage':
        
        latlon = [float(coord) for coord in sys.argv[2:4]]
        urls = intake.Url(**config.url_args, latlon=latlon).return_urls()
        autotile_kwargs = {
            'urls' : urls,
            'location' : latlon,
            'tooltip' : f"'{sys.argv[4]}'",
            'tiles' : config.tiles,
        }
        at = AutoTile(**autotile_kwargs)
        at.write_toa_tiffs()
        at.render_streamlit_view()

    elif sys.argv[1] == 'tune':

        subprocess.run(['panel', 'serve', 'tune.py', '--show'])

    elif sys.argv[1] == 'optimize':

        o = OptimizedIngest()
        o.optimize_tiffs_as_cogs()
        scenes = ['center',]
        for s in scenes:
            o.ingest_cogs_to_sqlite(scene_id=s)

    elif sys.argv[1] == 'serve':

        subprocess.run(["./scripts/serve.sh"])

    elif sys.argv[1] == 'down':

        subprocess.run(["./scripts/down.sh"])

    elif sys.argv[1] == 'reset':

        subprocess.run(["./scripts/reset_geotiffs.sh"])

    else:

        valids = ('stage', 'tune', 'optimize', 'serve', 'down', 'reset')

        logger.warning( 
            "Invalid arg: '%s'. Must be one of %s" % (sys.argv[1], valids)
        )