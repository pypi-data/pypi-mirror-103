from Xlib import X, XK
from Xlib.ext import record
from Xlib.display import Display
from Xlib.protocol import rq

from .snap import snap_window, shift_window
from .zoning import ZoneProfile
from .conf.settings import SETTINGS

class Service:
    def __init__(self) -> None:
        self.active_keys = {
            XK.string_to_keysym(key): False 
            for key in SETTINGS.keybindings
        }
        self.zp = ZoneProfile.from_file()

        self.display = Display()
        self.root = self.display.screen().root
        
        self.context = self.display.record_create_context(0, [record.AllClients], [{
            'core_requests': (0, 0),
            'core_replies': (0, 0),
            'ext_requests': (0, 0, 0, 0),
            'ext_replies': (0, 0, 0, 0),
            'delivered_events': (0, 0),
            'device_events': (X.KeyReleaseMask, X.ButtonReleaseMask),
            'errors': (0, 0),
            'client_started': False,
            'client_died': False,
        }])

        self.display.record_enable_context(self.context, self.handler)
        self.display.record_free_context(self.context)
        
    def handler(self, reply):
        data = reply.data
        while len(data):

            event, data = rq.EventField(None).parse_binary_value(data, self.display.display, None, None)
                
            if event.type == X.KeyPress or X.KeyRelease:
                keysym = self.display.keycode_to_keysym(event.detail, 0)
                if keysym in self.active_keys:
                    self.active_keys[keysym] = (
                        True if event.type == X.KeyPress else False
                    )

            if all([value == True for value in self.active_keys.values()]):

                if event.type == X.ButtonRelease:
                    snap_window(self, event.root_x, event.root_y)

                elif event.type == X.KeyPress:
                    keysym = self.display.keycode_to_keysym(event.detail, 0)
                    shift_window(self, keysym)

    def listen(self):
        while True:
            self.root.display.next_event()