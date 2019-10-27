import logging

import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.hw.base import DisplayImpl


class NoScreen(DisplayImpl):
    def __init__(self, config):
        super(NoScreen, self).__init__(config, 'noscreen')
        self._display = None

    def layout(self):
        fonts.setup(10, 9, 10, 35)
        self._layout['width'] = 250
        self._layout['height'] = 122
        self._layout['face'] = (0, 40)
        self._layout['name'] = (5, 20)
        self._layout['channel'] = (0, 0)
        self._layout['aps'] = (28, 0)
        self._layout['uptime'] = (185, 0)
        self._layout['line1'] = [0, 14, 250, 14]
        self._layout['line2'] = [0, 108, 250, 108]
        self._layout['friend_face'] = (0, 92)
        self._layout['friend_name'] = (40, 94)
        self._layout['shakes'] = (0, 109)
        self._layout['mode'] = (225, 109)
        self._layout['status'] = {
            'pos': (125, 20),
            'font': fonts.Medium,
            'max': 20
        }
        return self._layout

    def initialize(self):
        logging.info("initializing noscreen display")

    def render(self, canvas):
        return self

    def clear(self):
        logging.info("clear noscreen display")
