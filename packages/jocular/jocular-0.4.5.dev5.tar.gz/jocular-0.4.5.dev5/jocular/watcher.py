''' Monitors any incoming subs
'''

import os
import numpy as np

from kivy.logger import Logger
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ConfigParserProperty, BooleanProperty

from skimage.transform import rescale, downscale_local_mean

from jocular.component import Component
from jocular.utils import move_to_dir
from jocular.image import Image, ImageNotReadyException, is_fit, save_image

class Watcher(Component):

    # new in v0.5
    bayerpattern = ConfigParserProperty('mono', 'Watcher', 'bayerpattern', 'app', val_type=str)
    binfac_on_input = ConfigParserProperty(1, 'Watcher', 'binfac_on_input', 'app', val_type=int)
    binmethod = ConfigParserProperty('interpolate', 'Watcher', 'binmethod', 'app', val_type=str)
    save_originals = ConfigParserProperty(1, 'Watcher', 'save_originals', 'app', val_type=int)
    
    # set to True if capture mode is Watched and user is capturing
    capturing = BooleanProperty(False)

    def __init__(self):
        super(Watcher, self).__init__()
        self.watched_dir = App.get_running_app().get_path('watched')
        self.watching_event = Clock.schedule_interval(self.watch, .3)

    def on_new_object(self):
        self.flush()

    def on_close(self):
        self.watching_event.cancel()
        self.flush()    # user has had enough so move any FITs to delete

    def flush(self):
        # move any FITs that are not masters to a 'unused' folder in watcher
        # (masters are saved immediately before new object, so risk they are not spotted in time!)
        for f in os.listdir(self.watched_dir):
            if is_fit(f):
                if not f.startswith('master'):
                    move_to_dir(os.path.join(self.watched_dir, f), 'unused')

    def get_possible_fits(self):
        fits = [os.path.join(self.watched_dir, d) for d in os.listdir(self.watched_dir)]
        # for ASIlive look deeper
        asipath = os.path.join(self.watched_dir, 'ASILive_AutoSave', 'SingleFrame')
        if os.path.exists(asipath):
            for sdir in os.listdir(asipath):
                pth = os.path.join(asipath, sdir)
                if os.path.isdir(pth):
                    fits += [os.path.join(pth, d) for d in os.listdir(pth)]
        return fits

    def watch(self, dt):
        '''Watcher handles two types of event:

            1.  Users drop individual subs (manually or via a capture program); if
                validated these are passed to ObjectIO
            2.  Users drop master calibration frames; if validated, passed to Calibrator
                to become part of the library and become available for immediate use

            Validated files are removed from 'watched'. If not validated, files are
            either left to be re-handled on the next event cycle, or moved to 'invalid'.
            Non-fits files are moved to 'ignored'
        '''

        ''' New approach with WatchedCamera is to allow through all Jocular-created subs
            but only allow through alien subs if WatchedCamera is capturing. Rest are
            shunted off to ignored.
        '''

        for path in self.get_possible_fits():
            f = os.path.basename(path)
            if is_fit(f):
                try:
                    s = Image(path, check_image_data=True)

                    # captured natively so let it through
                    if s.created_by_jocular:
                        if s.is_master:
                            Component.get('Calibrator').new_master_from_watcher(s)
                        else:
                            Component.get('ObjectIO').new_sub_from_watcher(s)

                    # watcher is not allowing stuff in
                    elif not self.capturing:
                        move_to_dir(path, 'ignored')

                    # non-jocular FITs are converted to Jocular FITs, spat back out to Watched
                    # directory, and the originals saved if required
                    else:
                        self.process_alien_sub(s, path)
 
                except ImageNotReadyException as e:
                    # give it another chance on next event cycle
                    Logger.debug('Watcher: image not ready {:} ({:})'.format(f, e))

                # added in v0.4.5 to catch error thrown by new_master    
                except IOError as e:
                    Logger.debug('Watcher: {:}'.format(e))
                    move_to_dir(path, 'invalid')

                except Exception as e:
                    # irrecoverable, so move to invalid, adding timestamp
                    Logger.debug('Watcher: other issue {:} ({:})'.format(f, e))
                    move_to_dir(path, 'invalid')

            elif not os.path.isdir(path):
                move_to_dir(path, 'nonfits')


    def bin(self, im):
        binfac = int(self.binfac_on_input)
        if binfac < 2:
            return im
        if self.binmethod == 'interpolation':
            return rescale(im, 1 / binfac, anti_aliasing=True, mode='constant', 
                preserve_range=True, multichannel=False)
        return downscale_local_mean(im, (binfac, binfac))

    def process_alien_sub(self, s, path):

        bn = os.path.basename(path)
        im = s.get_image()

        # don't debayer if mono or if it is a master calibration frame
        if self.bayerpattern == 'mono' or s.is_master:
            self.save_mono(s, self.bin(im), bn, filt=None)

        # debayer
        else:
            from colour_demosaicing import demosaicing_CFA_Bayer_bilinear
            rgb = demosaicing_CFA_Bayer_bilinear(im, pattern=self.bayerpattern)
            # rescale to original intensity range
            cfa_min, cfa_max = np.min(im), np.max(im)
            rgb_min, rgb_max = np.min(rgb), np.max(rgb)
            rgb = cfa_min + (cfa_max - cfa_min) * (rgb - rgb_min) / (rgb_max - rgb_min)
            for i, chan in enumerate(['R', 'G', 'B']):
                self.save_mono(s, self.bin(rgb[:, :, i]), bn, filt=chan)
 
        if self.save_originals and path is not None:
            Component.get('ObjectIO').save_original(path)


    def save_mono(self, sub, im, nm, filt=None):
        ''' Save image, binning if required, constructing details from Image instance
        '''

        details = Component.get('Capture').get_capture_details()

        filt = sub.filter if filt is None else filt
        filt = details['filter'] if filt is None else filt
        sub_type = details['sub_type'] #  if sub.sub_type is None else sub.sub_type
        exposure = details['exposure'] if sub.exposure is None else sub.exposure 
        temperature = sub.temperature

        if sub.is_master:
            save_image(data=im,
                path=os.path.join(self.watched_dir, 'master{:}.fit'.format(sub_type)),
                exposure=exposure, filt=filt, temperature=temperature, sub_type='master ' + sub_type,
                nsubs=sub.nsubs)
        else:
            save_image(data=im.astype(np.uint16), 
                path=os.path.join(self.watched_dir, '{:}_{:}'.format(filt, nm)),
                filt=filt, sub_type=sub_type, exposure=exposure, temperature=temperature)
