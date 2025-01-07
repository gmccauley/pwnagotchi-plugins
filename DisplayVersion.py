from pwnagotchi.ui.components import Text
from pwnagotchi.ui.view import BLACK
import pwnagotchi.plugins as plugins
import pwnagotchi.ui.fonts as fonts
import pwnagotchi
import logging


class PwnagotchiVersion(plugins.Plugin):
    __author__ = 'https://github.com/gmccauley/'
    __version__ = '2.0.0'
    __license__ = 'GPL3'
    __description__ = 'A plugin that will add the Pwnagotchi version in a configurable location.'

    def __init__(self):
        self.options = dict()

    def on_loaded(self):
        logging.info('[DisplayVersion] plugin loaded.')

    def on_ui_setup(self, ui):
        ver = 'v' + str(pwnagotchi.__version__)
        #ver = 'v1.2.3.4.5.6'
        logging.info('[DisplayVersion] Version = ' + ver)

        if 'position' in self.options and self.options['position'] is not None:
            logging.info('[DisplayVersion] Using position in config.toml')
            posX = int(self.options['position'].split(',')[0].strip())
            posY = int(self.options['position'].split(',')[1].strip())
        else:
        #if True:
            logging.info('[DisplayVersion] Using default position')
            posX = ui._width - ((len(ver)) * 5.5)
            posY = ui._layout['line2'][3] - 10
        logging.info('[DisplayVersion] Position = (' + str(posX) + ',' + str(posY) + ')')

        ui.add_element(
            'version',
            Text(
                color=BLACK,
                value=ver,
                position=(posX, posY),
                font=fonts.Small
            )
        )
