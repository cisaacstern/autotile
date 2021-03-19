import sys

#import jinja

import config
import intake
#from tune import Tune
#from view import View

class AutoTile(intake.Intake): #, Tune, View):

    def __init__(self, **kwargs):
        super(AutoTile, self).__init__(**kwargs)

    def stage_tiffs(self):
        '''
        '''
        self.request_tiffs()
        self.save_toa_tiffs()

    def render_html(self):
        '''
        '''
        pass
    
if __name__ == '__main__':

    if sys.argv[1] == 'tune':

        print('Tune!')
    
    elif sys.argv[1] == 'stage':

        urls = intake.Url(**config.url_args).return_urls()

        #arguments = [float(arg) for arg in sys.argv[1:3] else arg]
        #arguments[3] = strptime(arguments[3])
        #arguments.pop(0)

        #assert arguments[0] in np.range(), "This must be a latitude."
        #assert arguments[1] in np.range(), "This must be a latitude."
        #assert arguments[2] in STACJSON, "Not a valid time."

        at = AutoTile(urls=urls, label=sys.argv[2])
        at.stage_tiffs()
        #at.render_html()

        #subprocess.run[".", "./scripts/stage.sh"]

    elif sys.argv[1] == 'serve':

        #subprocess.run[".", "./scripts/serve.sh"]
        print('Serve!')

    elif sys.argv[1] == 'down':

        #subprocess.run[".", "./scripts/down.sh"]
        print('Down!')

    else:

        valids = ('tune', 'stage', 'serve', 'down')

        logger.WARNING(
            "%s invalid as 1st arg. Must be one of %s", (sys.argv[0], valids)
        )