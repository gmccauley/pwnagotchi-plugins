from pwnagotchi.ui.components import Bitmap
from pwnagotchi.ui.view import BLACK
from pwnagotchi.ui.view import View
import pwnagotchi.plugins as plugins
import pwnagotchi.ui.fonts as fonts
import pwnagotchi, logging, os, base64, socket


class InternetConnection(plugins.Plugin):
    __author__ = 'https://github.com/gmccauley/'
    __version__ = '2.0.0'
    __license__ = 'GPL3'
    __description__ = 'A plugin that will add an icon when internet connection is available'

    def __init__(self):
        self.options = dict()
        self.connectionState = False
        if self.invert():
            self.iconPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "internet-conection-invert.png")
            self.iconContent = 'iVBORw0KGgoAAAANSUhEUgAAAAoAAAAJCAIAAACExCpEAAAARklEQVR4nHWPQQ4AIQgDp8b/f7l7ULGRLCdow1BkGwAkcarEWV5JOY7ure0Ls93tpey9P/hOkYDqbSuTd9LoyTPXezKfBj5LFU3jH0NO3gAAAABJRU5ErkJggg=='
        else:
            self.iconPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "internet-conection.png")
            self.iconContent = 'iVBORw0KGgoAAAANSUhEUgAAAAoAAAAJCAIAAACExCpEAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABBSURBVChTdYxJDgAwCALx/4+2NHRR0s5FFkNgk5lLARE3n9SONGudUBg8mqpPnthAs8dQVC2x+BbEoscHYdoKYADotjvQHzauBAAAAABJRU5ErkJggg=='

    def on_loaded(self):
        logging.info('[InternetConnection] plugin loaded.')
        logging.info('[InternetConnection] Icon Path = ' + self.iconPath)
        if os.path.isfile(self.iconPath):
            logging.info('[InternetConnection] Icon Exists')
        else:
            logging.info('[InternetConnection] Icon Not Found...  Creating')
            try:
                with open(self.iconPath, 'wb') as file:
                    file.write(base64.b64decode(self.iconContent))
            except Exception as e:
                logging.info('[InternetConnection] ' + str(e))

    def on_ui_setup(self, ui):
        if 'position' in self.options and self.options['position'] is not None:
            logging.info('[InternetConnection] Using position in config.toml')
            self.posX = int(self.options['position'].split(',')[0].strip())
            self.posY = int(self.options['position'].split(',')[1].strip())
        else:
            logging.info('[InternetConnection] Using default position')
            self.posX = (ui._width // 2) - 25
            self.posY = 2
        logging.info('[InternetConnection] Position = (' + str(self.posX) + ',' + str(self.posY) + ')')

    def on_ui_update(self, ui):
        newState = self._is_internet_available()
        if newState != self.connectionState:
            self.connectionState = newState
            if self.connectionState:
                logging.info('[InternetConnection] Connection Established.  Showing Icon')
                ui.add_element(
                    'internetConnection',
                    Bitmap(
                        color=BLACK,
                        path=self.iconPath,
                        xy=(self.posX, self.posY)
                    )
                )
            else:
                logging.info('[InternetConnection] Connection Broken.  Removing Icon')
                ui.remove_element('internetConnection')

    def on_unload(self, ui):
        ui.remove_element('internetConnection')


    def _is_internet_available(self):
        try:
            socket.create_connection(("www.google.com", 80), timeout=0.5)
            return True
        except OSError:
            return False

    def invert(self):
        try:
            with open("/etc/pwnagotchi/config.toml", "r") as f:
                config = f.readlines()
        except FileNotFoundError:
            logging.warning("[InternetConnection] Config File not found")
            return False
        except EOFError:
            pass
        for line in config:
            line = line.strip()
            line = line.strip('\n')
            if "ui.invert = true" in line or "ui.invert = false" in line:
                if line.find("ui.invert = true") != -1:
                    logging.debug("[InternetConnection] Screen Invert True")
                    return True
                elif line.find("ui.invert = false") != -1:
                    logging.debug("[InternetConnection] Screen Invert False")
                    return False
        return False
