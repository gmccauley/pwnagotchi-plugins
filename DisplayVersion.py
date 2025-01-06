from pwnagotchi.ui.components import LabeledValue
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

    DEFAULT_POSITION = [150, 100]
    
    def on_loaded(self):
        logging.info('[DisplayVersion] plugin loaded.')
        
    def on_ui_setup(self, ui):
        try:
            pos = self.options['position'].split(',')
            pos = [int(x.strip()) for x in pos]
        except Exception:
            pos = DEFAULT_POSITION
        ui.add_element(
            'version',
            LabeledValue(
                color=BLACK,
                label='',
                value='v0.0.0',
                position=(pos[0], pos[1]),
                label_font=fonts.Small,
                text_font=fonts.Small
            )
        )

    def on_ui_update(self, ui):
        ui.set('version', f'v{pwnagotchi.__version__}')
