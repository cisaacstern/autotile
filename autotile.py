import sys
import subprocess
import logging

from jinja2 import Environment, FileSystemLoader

import config
import intake
#from view import View

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
        filepattern = '$NOT_MATCHED/' + scene_id + "_{band}.tif"
        cmd = f"terracotta ingest {filepattern} -o _notmatched.sqlite"
        subprocess.Popen(cmd, shell=True)

    
if __name__ == '__main__':
    
    if sys.argv[1] == 'stage':
        
        autotile_kwargs = {
            'urls' : intake.Url(**config.url_args).return_urls(),
            'location' : [float(coord) for coord in sys.argv[2:4]],
            'tooltip' : f"'{sys.argv[4]}'",
            'tiles' : config.tiles,
        }
        at = AutoTile(**autotile_kwargs)
        at.write_toa_tiffs()
        at.render_streamlit_view()

    elif sys.argv[1] == 'tune':

        subprocess.run(['panel', 'serve', 'tune.py', '--show'])

    elif sys.argv[1] == 'match':

        pass

    elif sys.argv[1] == 'optimize':

        o = OptimizedIngest()
        o.optimize_tiffs_as_cogs()
        scenes = ['center',]
        for s in scenes:
            o.ingest_cogs_to_sqlite(scene_id=s)

    elif sys.argv[1] == 'serve':

        subprocess.run(["./scripts/serve.sh"])
        # subprocess.run(["streamlit", "run", "_rendered_view.py"])

    elif sys.argv[1] == 'down':

        #subprocess.run[".", "./scripts/down.sh"]
        print('Down!')

    else:

        valids = ('tune', 'stage', 'serve', 'down')

        logger.WARNING(
            "%s invalid as 1st arg. Must be one of %s", (sys.argv[0], valids)
        )