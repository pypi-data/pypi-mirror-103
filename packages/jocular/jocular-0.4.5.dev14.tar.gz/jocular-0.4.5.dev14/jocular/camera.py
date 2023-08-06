''' Virtual and real camera classes, all subclasses of GenericCamera.
    For the moment there is quite a lot of factorisable repetition
    but once development has slowed down that can be dealt with ;-)
'''

import time
import array
import os
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from functools import partial

import zwoasi as asi

from kivy.logger import Logger
from kivy.app import App
from kivy.properties import BooleanProperty, ConfigParserProperty

from kivy.clock import Clock
from kivy.event import EventDispatcher

from jocular.component import Component


class GenericCamera(EventDispatcher):

    camera_connected = BooleanProperty(False)

    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller

    def reset(self):
        pass
    def on_close(self):
        pass
    def pause(self):
        pass
    def get_image(self):
        return None
    def connect(self):
        pass
    def is_connected(self):
        return self.camera_connected
    def select(self):
        pass
    def deselect(self):
        pass
    def on_new_object(self):
        pass
    def capture_sub(self, **kwargs):
        return None


class ASICamera(GenericCamera):

    def reset(self):
        self.connect()
        self.last_capture = None
        self.pause()

    def on_new_object(self):
        if not Component.get('ObjectIO').existing_object:
            Component.get('Capture').enable_captures()

    def select(self):
        if not Component.get('ObjectIO').existing_object:
            self.on_new_object()

    def connect(self):
        if self.camera_connected:
            return
            
        self.camera_connected = False
        self._camera = None

        try:
            asipath = App.get_running_app().get_path('ASICamera2.dll')
            if not os.path.exists(asipath):
                Logger.error('Camera: cannot find ASICamera2.dll in resources')
                return
        except Exception as e:
            Logger.error('Camera: problem getting asipath ({:})'.format(e))
            return

        try:
            asi.init(os.path.abspath(asipath))
        except Exception as e:
            Logger.error('Camera: problem initialising asi ({:})'.format(e))
            return

        try:
            num_cameras = asi.get_num_cameras()
            if num_cameras == 0:
                Logger.error('Camera: no cameras found')
                return
        except Exception as e:
            Logger.error('Camera: problem getting number of cameras ({:})'.format(e))
            return

        # get first camera found
        try:
            self._camera = asi.Camera(0)
        except Exception as e:
            Logger.error('Camera: problem assigning camera 0 ({:})'.format(e))
            return

        # if we want camera info we can get it using
        # camera_info = self._camera.get_camera_property()

        # set some properties: in future will be options
        try:
            self._camera.set_control_value(asi.ASI_BANDWIDTHOVERLOAD, 
                self._camera.get_controls()['BandWidth']['MinValue'])
            self._camera.disable_dark_subtract()
            self._camera.set_image_type(asi.ASI_IMG_RAW16)
            self._camera.set_control_value(asi.ASI_GAIN, 150)
        except Exception as e:
            Logger.error('Camera: problem setting control values ({:})'.format(e))
            return

        Logger.info('Camera: connected!')
        self.camera_connected = True

    def handle_failure(self, message='camera problem'):
        Logger.error('Camera: handling failure {:}'.format(message))
        self.camera_connected = False  # to ensure reconnect if that was the issue
        self.last_capture = None
        if self.on_failure is not None:
            self.on_failure()

    def get_image(self):
        return self.last_capture

    def capture_sub(self, exposure=None, on_capture=None, on_failure=None,
        binning=None, internal_timing=False, return_image=False, is_bias=False):

        if is_bias:
            self.exposure = .001

        self.exposure = exposure
        self.on_failure = on_failure
        self.on_capture = on_capture

        # exposure is in microseconds
        self._camera.set_control_value(asi.ASI_EXPOSURE, int(self.exposure * 1e6))
        Logger.debug('Camera: starting exposure')
        self._camera.start_exposure()

        if return_image:
            time.sleep(self.exposure)
            ready = False
            while not ready:
                time.sleep(.2)
                ready = self._camera.get_exposure_status() != asi.ASI_EXP_WORKING
            if self._camera.get_exposure_status() != asi.ASI_EXP_SUCCESS:
                self.handle_failure('capture problem')
                return
            return self.get_camera_data()
             
        self.capture_event = Clock.schedule_once(self.check_exposure, 
            max(0.2, self.exposure))

    def get_camera_data(self):
        # from https://github.com/stevemarple/python-zwoasi/blob/master/zwoasi/__init__.py
        data = self._camera.get_data_after_exposure(None)
        whbi = self._camera.get_roi_format()
        shape = [whbi[1], whbi[0]]
        img = np.frombuffer(data, dtype=np.uint16)
        return img.reshape(shape) / 2 ** 16

    def check_exposure(self, *arg):
        if self._camera.get_exposure_status() != asi.ASI_EXP_WORKING:
            self.last_capture = self.get_camera_data()
            if self.on_capture is not None:
                Clock.schedule_once(self.on_capture, 0)
        else:
            # check exposure again in 200 ms
            self.capture_event = Clock.schedule_once(self.check_exposure, 0.2)

    def pause(self):
        # Cancel any pending reads
        if hasattr(self, '_camera') and self._camera is not None:
            self._camera.stop_exposure()
        if hasattr(self, 'capture_event'):
            self.capture_event.cancel()



class AscomCamera(GenericCamera):

    def reset(self):
        self.connect()
        self.last_capture = None
        self.pause()

    def on_new_object(self):
        if not Component.get('ObjectIO').existing_object:
            Component.get('Capture').enable_captures()

    def select(self):
        if not Component.get('ObjectIO').existing_object:
            self.on_new_object()

    def connect(self):
        if self.camera_connected:
            if hasattr(self, '_camera') and self._camera.connected:
                return
            
        self.camera_connected = False
        self._camera = None

        try:
            import win32com.client
        except Exception as e:
            Logger.error('Camera: cannot import win30com.client: ({:})'.format(e))
            return

        try:
            x = win32com.client.Dispatch("ASCOM.Utilities.Chooser")
            x.DeviceType = 'Camera'
            driver = x.Choose(None)
            Logger.info('Camera: got driver {:}'.format(driver))
            camera = win32com.client.Dispatch(driver)
            Logger.info('Camera: dispatched driver {:}'.format(camera))
            self._camera = camera
            Logger.info('Camera: assigned driver to _camera')
            self._camera.connected = True   # this is camera-specific prop
            Logger.info('Camera: set connected on driver to True')
            self.camera_connected = True    # note this is generic prop
        except Exception as e:
            Logger.error('Camera: problem connecting ASCOM camera: ({:})'.format(e))
            return

        Logger.info('Camera: ASCOM camera connected')

    def handle_failure(self, message='camera problem'):
        Logger.error('Camera: handling failure {:}'.format(message))
        self.camera_connected = False  # to ensure reconnect if that was the issue
        self.last_capture = None
        if self.on_failure is not None:
            self.on_failure()

    def get_image(self):
        return self.last_capture

    def capture_sub(self, exposure=None, on_capture=None, on_failure=None,
        binning=None, internal_timing=False, return_image=False, is_bias=False):

        self.exposure = exposure
        self.on_failure = on_failure
        self.on_capture = on_capture

        if is_bias:
            self.exposure = .001
            openshutter = False
        else:
            openshutter = True

        self._camera.startExposure(self.exposure, openshutter) 

        if return_image:
            time.sleep(self.exposure)
            ready = False
            while not ready:
                time.sleep(.2)
                ready = self._camera.ImageReady
            return self.get_camera_data()

        self.capture_event = Clock.schedule_once(self.check_exposure, 
            max(0.2, self.exposure))

    def check_exposure(self, *arg):
        if self._camera.ImageReady:
            self.last_capture = self.get_camera_data()
            if self.on_capture is not None:
                Clock.schedule_once(self.on_capture, 0)
        else:
            # check exposure again in 200 ms
            self.capture_event = Clock.schedule_once(self.check_exposure, 0.2)

    def get_camera_data(self):
        # data is ready so get it, convert to correct size, and scale to range 0-1
        # assumes 16 bits for now
        im = np.array(self._camera.ImageArray)
        shape = [self._camera.CameraYSize, self._camera.CameraXSize]
        return img.reshape(shape) / 2 ** 16

    def pause(self):
        # Cancel any pending reads
        Logger.debug('Camera: pause called')
        if hasattr(self, '_camera') and self._camera is not None:
            # occasionally objects to being aborted
            if self._camera.CanStopExposure:
                Logger.debug('Camera: can stop exposure, trying')
                try:
                    self._camera.StopExposure()
                    Logger.debug('Camera: stopped exposure')
                except Exception as e:
                    Logger.error('Camera: unable to stop exposure ({:})'.format(e))
        if hasattr(self, 'capture_event'):
            self.capture_event.cancel()


''' ------------ SX cameras (just Lodestar for now)
'''

SX_CLEAR_PIXELS = 1
SX_READ_PIXELS_DELAYED = 2
SX_READ_PIXELS = 3
SX_RESET = 6

# convert int formats
def convert_int(x, from_type='uint16', to_type='uint8'):
    return np.array([x], dtype=from_type).view(dtype=to_type)

class SXCamera(GenericCamera):

    def reset(self):
        self.connect()
        self.last_capture = None
        self.pause()

    def on_new_object(self):
        if not Component.get('ObjectIO').existing_object:
            Component.get('Capture').enable_captures()

    def select(self):
        if not Component.get('ObjectIO').existing_object:
            self.on_new_object()

    def pause(self):
        # Cancel any pending reads
        if hasattr(self, 'capture_event'):
            if not self.internal_timing:  
                # don't cancel reading if using internal timing (causes crash on LS)
                self.capture_event.cancel()

    def clean_up(self):
        if hasattr(self, 'lodestar'):
            import usb.util
            usb.util.dispose_resources(self.lodestar)
            Logger.debug('Camera: disposed')

    def handle_failure(self, message='camera problem'):
        Logger.error('Camera: handle_failure {:}'.format(message))
        self.camera_connected = False  # to ensure reconnect if that was the issue
        self.last_capture = None
        try:
            self.clean_up()
        except Exception as e:
            Logger.warn('Camera: problem disposing {:}'.format(e))
            self.contoller.warn('disconnected?')
        finally:
            if self.on_failure is not None:
                self.on_failure()

    def get_image(self):
        return self.last_capture

    def capture_sub(self, exposure=None, on_capture=None, on_failure=None,
        binning=None, internal_timing=False, return_image=False, is_bias=False):

        if is_bias:
            self.capture_bias(on_capture=on_capture, on_failure=on_failure)
            return

        # store these so they can be used without argument passing in futures etc
        self.on_capture = on_capture
        self.on_failure = on_failure
        self.exposure = exposure
        self.binning = binning
        self.internal_timing = internal_timing
        self.return_image = return_image
        self.last_capture = None

        # try to connect to camera (will handle if already connected)
        self.connect()

        if not self.camera_connected:
            self.handle_failure('camera not connected')
            return

        try:
            if internal_timing:
                # do internal_timed exposure
                self.start_internal_exposure()
                if return_image:
                    time.sleep(exposure)
                    return self.lodestar_read()
                else:
                    self.capture_event = Clock.schedule_once(
                        self.read_internal_exposure, max(0.1, exposure)
                    )
            else:
                # externally-timed
                self.start_external_exposure()
                if return_image:
                    time.sleep(exposure)
                    return self.read_external_exposure()
                else:
                    self.capture_event = Clock.schedule_once(
                        self.read_external_exposure, max(0.2, self.exposure)
                    )

        except Exception as e:
            self.handle_failure('capture problem {:}'.format(e))

    def capture_bias(self, on_capture=None, on_failure=None):
        # special case for bias as it needs even and odd for internally-timed exposure
        self.on_capture = on_capture
        self.on_failure = on_failure
        try:
            self.connect()
            expo = 0.001
            self.exposure_command(rows='odd', exposure=expo)
            time.sleep(expo)
            odd_pixels = self.lodestar.read(0x82, self.height * self.width, 10000)
            self.exposure_command(rows='even', exposure=expo)
            time.sleep(expo)
            even_pixels = self.lodestar.read(0x82, self.height * self.width, 10000)
            pool = ThreadPoolExecutor(3)
            future = pool.submit(
                partial(self.deinterlace, odd_pixels, even_pixels)
            )  # thread handles read
            future.add_done_callback(
                self.image_ready
            )  # when future is done, call image_ready
        except Exception as e:
            self.handle_failure('problem in capture_bias {:}'.format(e))

    def exposure_command(self, rows='odd', exposure=None):
        # generate write command for sensor
        try:
            rowcode = {'odd': 1, 'even': 2, 'all': 3}
            cmd = SX_READ_PIXELS if exposure is None else SX_READ_PIXELS_DELAYED
            params = array.array(
                'B',
                [
                    0x40, cmd, rowcode[rows], 0, 0, 0, 10, 0, 0, 0, 0, 0,
                    self.lswidth, self.mswidth, self.lsheight, self.msheight, 1, 1
                ],
            )
            if exposure is not None:
                # add exposure details to command
                expo = int(exposure * 1000)  #  ms
                exp1, exp2, exp3, exp4 = convert_int(expo, from_type='uint32')
                params = params + array.array('B', [exp1, exp2, exp3, exp4])
            self.lodestar.write(1, params, 1000)
        except Exception as e:
            self.handle_failure('problem in exposure_command {:}'.format(e))

    def start_internal_exposure(self):
        try:
            self.exposure_command(rows='odd', exposure=self.exposure)
        except Exception as e:
            self.handle_failure('problem in start_internal_exposure {:}'.format(e))

    def start_external_exposure(self):
        try:
            self.lodestar.ctrl_transfer(0x40, SX_RESET, 0, 0, 0)
            self.lodestar.ctrl_transfer(0x40, SX_CLEAR_PIXELS, 0, 0, 0)
            Logger.trace('Camera: started external exposure')
        except Exception as e:
            self.handle_failure('problem in start_external_exposure {:}'.format(e))

    def read_internal_exposure(self, *args):
        try:
            pool = ThreadPoolExecutor(3)
            future = pool.submit(self.lodestar_read)  # thread handles read
            future.add_done_callback(self.image_ready)  # when future is done, call image_ready
        except Exception as e:
            self.handle_failure('problem in read_internal_exposure {:}'.format(e))

    def read_external_exposure(self, *args):
        # Reads sensor at end of exposure time

        try:
            self.exposure_command(rows='odd')
            odds = self.lodestar.read(0x82, self.height * self.width, timeout=10000)
            self.exposure_command(rows='even')
            evens = self.lodestar.read(0x82, self.height * self.width, timeout=10000)

            # de-interlace to create final image
            self.last_capture = self.deinterlace(odds, evens)

            if self.on_capture is not None:
                self.on_capture()
        except Exception as e:
            self.handle_failure('problem in read_external_exposure {:}'.format(e))

    def lodestar_read(self):
        try:
            odd_pixels = self.lodestar.read(0x82, self.height * self.width, 10000)
            return self.deinterlace(odd_pixels, odd_pixels)
        except Exception as e:
            self.handle_failure('problem in lodestar_read {:}'.format(e))

    def image_ready(self, future):
        self.last_capture = future.result()  # store image read from sensor
        if self.on_capture is not None:
            Clock.schedule_once(self.on_capture, 0)

    def deinterlace(self, odd8, even8):
        '''De-interlaces Lodestar.'''

        # convert uint8 arrays to uint16 and reshape
        odd = np.frombuffer(odd8, dtype='uint16').reshape(self.half_height, self.width)
        even = np.frombuffer(even8, dtype='uint16').reshape(self.half_height, self.width)

        # generate new array (full height)
        pix = np.zeros((self.height, self.width))

        # insert odd rows
        pix[::2, :] = odd

        # insert even rows and normalise to account for slight delay in reading
        pix[1::2, :] = even * (np.mean(odd) / np.mean(even))

        return pix / 2 ** 16

    def connect(self):
        ''' Connect to Lodestar. For other SX cameras will need to change idProduct
            and check interface/endpoint details. Not working on Windows.
        '''

        if self.camera_connected:
            return

        if os.name == 'nt':
            self.info('not supported')
            return

        self.camera_connected = False

        try:
            import usb.core
            import usb.util
        except:
            self.controller.warn('no usb.core or usb.util')
            return

        self.lodestar = None
        try:
            self.lodestar = usb.core.find(idVendor=0x1278, idProduct=0x0507)
        except:
            self.controller.warn('cannot find camera')

        if self.lodestar is None:
            self.controller.info('not connected')
            return

        try:
            conf = self.lodestar.get_active_configuration()
        except Exception as e:
            Logger.warn('Camera: cannot get config ({:})'.format(e))
            self.controller.warn('no config')
            self.clean_up()
            return

        self.camera_connected = True
        self.controller.info('SX Lodestar')

        # used in capture; note h // 2 for interlaced; needs changing for ultrastar no doubt
        self.width, self.height = 752, 580
        self.half_height = self.height // 2
        self.lswidth, self.mswidth = convert_int(self.width)
        self.lsheight, self.msheight = convert_int(self.half_height)




''' This is a watched camera that is always on i.e. like the
    original watched folder arrangement. Have to ensure we disable
    the capture button and set capturing in Watcher to True throughout.
'''

class WatchedCamera(GenericCamera):
 
    def select(self):
        self.camera_connected = True    # effectively always true
        self.on_new_object()

    def deselect(self):
        ''' Stop watcher and capture capturing; any new camera mode selected
            is responsible for enabling capture controls
        '''
        Component.get('Watcher').capturing = False
        Component.get('Capture').capturing = False

    def on_new_object(self):
        # allow watcher to capture only if not viewing previous object
        Component.get('Capture').disable_captures()
        Component.get('Watcher').capturing = not Component.get('ObjectIO').existing_object   


''' A watched camera that responds to the capture start/stop toggle. Subs
    are only allowed through when capturing. Behaviour controlled by Watcher.
'''

class WatchedCameraOnOff(GenericCamera):

    def connect(self):
        self.on_new_object()

    def capture_sub(self, exposure=None, on_capture=None, on_failure=None, binning=None, 
                    internal_timing=False, return_image=False, is_bias=False):
        Component.get('Watcher').capturing = True

    def pause(self):
        Component.get('Watcher').capturing = False

    def reset(self):
        self.on_new_object()

    def select(self):
        self.on_new_object()

    def deselect(self):
        Component.get('Capture').disable_captures()

    def on_new_object(self):
        # allow watcher to capture only if not viewing previous object
        self.camera_connected = not Component.get('ObjectIO').existing_object
        if self.camera_connected:
            Component.get('Capture').enable_captures()
        

