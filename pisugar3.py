import logging
import struct
import time

from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.plugins as plugins
import pwnagotchi


class UPS:
    def __init__(self):
        import smbus
        self._bus = smbus.SMBus(1)
        self.sample_size = 25
        self.battery_readings = []

    def capacity(self):
        battery_level = 0
        try:
            battery_level = self._bus.read_byte_data(0x57, 0x2a)
        except:
            pass
        return battery_level

    def status(self):
        try:
            stat02 = self._bus.read_byte_data(0x57, 0x02)
            stat03 = self._bus.read_byte_data(0x57, 0x03)
            stat04 = self._bus.read_byte_data(0x57, 0x04)
        except:
            return None, None, None
        return stat02, stat03, stat04

    def smoothed_capacity(self):
        if len(self.battery_readings) < self.sample_size:
            self.battery_readings.append(self.capacity())
        else:
            self.battery_readings.pop(0)
            self.battery_readings.append(self.capacity())

        return int(sum(self.battery_readings) / len(self.battery_readings))


class PiSugar3(plugins.Plugin):
    __author__ = 'https://github.com/gmccauley/'
    __version__ = '2.0.0'
    __license__ = 'MIT'
    __description__ = 'A plugin that shows charging status and battery percentage for the PiSugar3'

    def __init__(self):
        self.ups = None
        self.lasttemp = 69
        self.drot = 0
        self.nextDChg = 0

    def on_loaded(self):
        self.ups = UPS()
        logging.info("[pisugar3] plugin loaded.")

    def on_ui_setup(self, ui):
        if 'position' in self.options and self.options['position'] is not None:
            logging.info('[pisugar3] Using position in config.toml')
            posX = int(self.options['position'].split(',')[0].strip())
            posY = int(self.options['position'].split(',')[1].strip())
        else:
            logging.info('[pisugar3] Using default position')
            posX = (ui._width // 2) + 20
            posY = 0
        logging.info('[pisugar3] Position = (' + str(posX) + ',' + str(posY) + ')')

        try:
            ui.add_element('bat', LabeledValue(color=BLACK, label='BAT', value='0',
                                               position=(posX, posY),
                                               label_font=fonts.Bold, text_font=fonts.Medium))
        except Exception as err:
            logging.warning("pisugar3 setup err: %s" % repr(err))

    def on_unload(self, ui):
        try:
            with ui._lock:
                ui.remove_element('bat')
        except Exception as err:
            logging.warning("pisugar3 unload err: %s" % repr(err))

    def on_ui_update(self, ui):
        capacity = self.ups.smoothed_capacity()
        status = self.ups.status()

        # If the battery is turned off, the status will display "NF", as in "Not Found".
        if status[0] == None:
            ui._state._state['bat'].label = "BAT"
            ui._state._state['bat'].value = "NF"
            # Write the status to the log, so we can see if the battery is turned off.
            # Using only a debug log, so it doesn't spam the log file.
            logging.debug('[pisugar3] No battery found')
            return

        if status[0] & 0x80:
            ui._state._state['bat'].label = "CHG"
        else:
            ui._state._state['bat'].label = "BAT"

        if capacity <= self.options['shutdown']:
            logging.info('[pisugar3] Empty battery (<= %s%%): shutting down' % self.options['shutdown'])
            ui.update(force=True, new_data={'status': 'Battery exhausted, bye ...'})
            pwnagotchi.shutdown()

        ui.set('bat', "%i" % capacity)
