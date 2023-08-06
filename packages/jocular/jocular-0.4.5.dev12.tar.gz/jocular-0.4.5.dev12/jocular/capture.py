''' Runs the capture scripts using generators.

    New in v0.5 is the selection of different capture modes e.g. 
    watched folder, native SX, ... with more to come. These are
    handled by the on_capture_mode method, otherwise no real
    changed here. Most of the changes are in Camera, which
    implements a subclass for each mode.
'''

import os
import time
import numpy as np
from scipy.interpolate import interp1d

from kivy.app import App
from kivy.properties import NumericProperty, BooleanProperty, ConfigParserProperty
from kivy.clock import Clock
from kivy.logger import Logger

from jocular.component import Component
from jocular.widgets import JPopup
from jocular.image import save_image
from jocular.gradient import image_stats
from jocular.camera import (
    GenericCamera, SXCamera, WatchedCamera, WatchedCameraOnOff,
    AscomCamera, ASICamera
    )

class Capture(Component):

    capturing = BooleanProperty(False)
    exposure = NumericProperty(0)
    scripts = [s + '_script' for s in {'seq', 'light', 'frame', 'dark', 'flat', 'bias'}]
    capture_mode = ConfigParserProperty(
        'watcher', 'Capture Modes', 'capture_mode', 'app', val_type=str)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.gui = self.app.gui
        self.camera = GenericCamera(self)
        self.last_mode = None
        self.modes = {}

    def on_new_object(self):
        self.reset()
        self.on_capture_mode() # set up capture mode
        self.camera.on_new_object()

    def on_capture_mode(self, *args):
        ''' Factory-style instantiation of object to represent camera.
            Caches objects for fast switching.
        '''

        #for k, v in self.modes.items():
        #    print('  mode {:} connected {:} active {:}'.format(k, v.is_connected(), k==self.capture_mode)) 

        if self.last_mode is not None and self.capture_mode == self.last_mode:
            return

        mode = self.capture_mode
        if self.last_mode is not None:
            self.modes[self.last_mode].deselect()
        self.last_mode = mode

        # if we already instantiated this mode, switch camera to it
        if mode in self.modes:
            self.camera = self.modes[mode]
            self.camera.select()
            Logger.info('Capture: Capture mode changed to cached {:}'.format(mode))
            self.info(mode)
            return

        # instantiate this mode if it is one we can handle
        if mode == 'native SX':
            c = SXCamera(self)
        elif mode == 'ASCOM':
            c = AscomCamera(self)
        elif mode == 'ASI':
            c = ASICamera(self)
        elif mode == 'watcher':
            c = WatchedCamera(self)
        elif mode == 'controllable watcher':
            c = WatchedCameraOnOff(self)
        else:
            Logger.info('Capture: Mode {:} not implemented'.format(mode))
            return

        Logger.info('Capture: Capture mode changed to {:}'.format(mode))
        self.info(mode)
        self.modes[mode] = c
        self.camera = c
        self.camera.select()

    def connect(self):
        self.camera.connect()

    def is_connected(self):
        return self.camera.is_connected()

    def pause(self):
        self.camera.pause()

    def reset(self):
        # to do: the camera should reset some of these things depending on its mode
        # to do: check this as it incorporates stuff from capture as well as camera 
        self.series_number = None
        self.stop_capture()
        self.gui.set('capturing', False)
        self.gui.enable(self.scripts + ['exposure_button', 'filter_button'])
        self.camera.reset()

    def get_image(self):
        return self.camera.get_image()

    def capture_sub(self, exposure=None, on_capture=None, on_failure=None, binning=None, 
                    internal_timing=False, return_image=False, is_bias=False):
        return self.camera.capture_sub(exposure=exposure, on_capture=on_capture,
                on_failure=on_failure, binning=binning, internal_timing=internal_timing,
                return_image=return_image, is_bias=is_bias)

    def on_close(self):
        self.camera.on_close()

    def disable_captures(self):
        self.gui.disable(self.scripts + ['capturing', 'exposure_button', 'filter_button'])

    def enable_captures(self):
        self.gui.enable(self.scripts + ['capturing', 'exposure_button', 'filter_button'])

    def soft_reset(self):
        # when stack is cleared we dont want full reset
        self.series_number = None

    def on_capturing(self, *args):
        # user (pressing camera button) or system changes capture state

        self.info('capturing' if self.capturing else 'paused')
        current_script = Component.get('CaptureScript').current_script

        if self.capturing:
            # user wants to capture, so check that camera is connected
            Logger.debug('Capture: check if camera is connected')
            if not self.camera.is_connected():
                self.camera.connect()
            if not self.camera.is_connected():
                self.gui.set('capturing', False, update_property=True)
                Logger.debug('Capture: cannot connect')
                # JBubble(message='No camera connected').open()
                return

            Logger.debug('Capture: camera connected, starting capture')

            # force user to pause/stop before changing any capture parameters
            self.gui.disable(self.scripts + ['exposure_button', 'filter_button', 'load_previous', 'new_DSO'])
            # enable current script so user can see what is being captures
            self.gui.enable(['{:}_script'.format(current_script)])
            try:
                self.capture()
            except Exception as e:
                Logger.error('Capture: problem capturing ({:})'.format(e))

        else:
            self.camera.pause()

            # we can always do framing
            self.gui.enable(['frame_script', 'exposure_button', 'filter_button', 'new_DSO'])
            # find out what stack contains
            subs = Component.get('Stacker').subs
            if len(subs) > 0:
                current = subs[0].sub_type
                if current == 'light':
                    self.gui.enable(['light_script', 'seq_script'])
                else:
                    self.gui.enable(['{:}_script'.format(current)])
            else:
                self.gui.enable(self.scripts + ['load_previous'])                   


    def stop_capture(self, *args):
        # called when problem capturing
        self.gui.set('capturing', False, update_property=True)
        self.gui.enable(self.scripts + ['exposure_button', 'filter_button'])

    def slew(self, *args):
        Logger.info('Capture: slew not implemented yet')

    def camera_disconnected(self):
        self.stop_capture()
        # temporarily comment this out as it should be done by the camera
        # self.gui.disable(['capturing'])

    def camera_reconnected(self):
        # temp comment out
        # self.gui.enable(['capturing'])
        pass

    def capture(self, *args):
        # generator yields next command to execute

        # check if user has pressed pause/stop
        if not self.capturing:
            return 

        # get next command from generator
        op = next(Component.get('CaptureScript').generator)

        if len(op) == 2:
            op, param = op

        # automatically change filter wheel, or request user to do so
        if op == 'set filter':
            Component.get('FilterWheel').select_filter(name=param, 
                changed_action=self.capture,
                not_changed_action=self.stop_capture)

        elif op == 'set exposure':
            self.exposure = param
            self.capture()

        # carry out a normal exposure
        elif op == 'expose long':
            try:
                self.info('capturing ...')
                self.camera.capture_sub(
                    exposure=self.exposure, 
                    on_capture=self.save_capture,
                    on_failure=self.stop_capture)
                if self.exposure > 2:
                    self.expo = self.exposure
                    self.exposure_start_time = time.time()
                    Clock.schedule_once(self.tick, 0)
                self.info('capturing')
            except Exception as e:
                Logger.error('Capture: problem in expose long {:}'.format(e))

        elif op == 'expose short':
            # we update info twice to ensure display updates...
            try:
                self.info('shorts ...')
                self.camera.capture_sub(
                    exposure=self.exposure, 
                    on_capture=self.send_to_display,
                    on_failure=self.stop_capture,
                    internal_timing=self.exposure < 1)
                self.info('shorts')
            except Exception as e:
                Logger.error('Capture: problem in expose short {:}'.format(e))

        elif op == 'expose bias':
            self.camera.capture_sub(
                on_capture=self.save_capture,
                on_failure=self.stop_capture,
                is_bias=True)
            self.info('capturing bias')

        elif op == 'autoflat':
            auto_expo = self.get_flat_exposure()
            if auto_expo is not None:
                self.exposure = auto_expo
                self.capture()
            else:
                self.stop_capture()
                # self.capturing = False

    def on_exposure(self, *args):
        Component.get('CaptureScript').set_exposure_button(self.exposure)        

    # move this to camera or count up?
    def tick(self, *args):
        # remaining = self.expo - (time.time() - self.exposure_start_time)
        dur = time.time() - self.exposure_start_time
        if self.capturing:
            self.info('Exposing {:2.0f}s'.format(dur))
            Clock.schedule_once(self.tick, 1)

    def send_to_display(self, *args):
        # send short subs directly to display
        try:
            Component.get('Monochrome').display_sub(self.camera.get_image())
            self.capture()
        except Exception as e:
            Logger.error('Capture: problem send to display {:}'.format(e))

    def get_capture_details(self):
        sub_type = Component.get('CaptureScript').current_script
        if sub_type == 'seq':
            sub_type = 'light'
        return {
            'exposure': self.exposure,
            'filter': Component.get('FilterWheel').current_filter,
            'sub_type': sub_type,
            'temperature': Component.get('Session').temperature
            }

    def save_capture(self, *args):
        ''' Called via camera when image is ready.
        '''

        # im = Component.get('Camera').get_image()
        im = self.camera.get_image()

        if im is None:
            self.warn('No image')
            return

        # we'll save as 16-bit int FITs
        im *= (2**16 - 1)

        details = self.get_capture_details()

        # sub_type = Component.get('CaptureScript').current_script
        # if sub_type == 'seq':
        #     sub_type = 'light'

        if not hasattr(self, 'series_number') or self.series_number is None:
            self.series_number = 1
        else: 
            self.series_number += 1

        sub_type = details['sub_type']

        filt = Component.get('FilterWheel').current_filter
        pref = sub_type if sub_type in {'flat', 'dark'} else details['filter']
        name = '{:}_{:d}.fit'.format(pref, self.series_number)

        save_image(data=im.astype(np.uint16),
            path=os.path.join(self.app.get_path('watched'), name),
            exposure=details['exposure'],
            filt=filt,
            temperature=details['temperature'],
            sub_type=sub_type)

        # ask for next capture immediately
        self.capture()

    def get_flat_exposure(self):
        # make a series of test exposures to get ADU just over half-way (0.5)

        min_exposure, max_exposure = 1, 2.5
        min_ADU, max_ADU = .3, .8

        expos = np.linspace(min_exposure, max_exposure, 5)
        adus = np.ones(len(expos))      # normalised ADUs actually
        for i, expo in enumerate(expos):
            # im = Component.get('Camera').capture_sub(exposure=expo, 
            im = self.camera.capture_sub(exposure=expo, 
                return_image=True,
                internal_timing=True,
                on_failure=self.stop_capture)

            # analyse image
            stats = image_stats(im)
            adus[i] = stats['central 75%']
            Logger.debug('Capture: autoflat exposure {:.1f}s has ADU of {:.2f}'.format(expo, adus[i]))

        # are any within ADU tolerance?
        if np.min(adus) > max_ADU:
            JPopup(title='Too early to collect flats', cancel_label='close').open()
            return None

        if np.max(adus) < min_ADU:
            JPopup(title='Too late to collect flats', cancel_label='close').open()
            return None

        # we are OK, so interpolate to get things purrrrfect
        f = interp1d(expos, adus)
        adu_target = .7
        xvals = np.linspace(min_exposure, max_exposure, 500)
        best = np.argmin(np.abs(adu_target - f(xvals)))
        best_exposure = xvals[best]
        Logger.debug('Capture: best exposure for autoflat {:} with ADU {:}'.format(best_exposure, f(best_exposure)))
        return float(best_exposure)
