from datetime import datetime
import time
from picamera import PiCamera


class Camera:
    def __init__(self, config, logger):
        self.logger = logger
        self.lock_camera = True
        self.num_shots_per_take = config['camera']['num_shots_per_take'] or 5
        self.pics_dir = config['pic_temp_dir'] or './'
        self.res_horizontal = config['camera']['resolution_horizontal'] or 1280
        self.res_vertical = config['camera']['resolution_vertical'] or 720
        self.framerate = config['camera']['framerate'] or 30
        self.iso = config['camera']['iso'] or 600
        self.logger.log('Initializing camera module')
        camera = PiCamera(resolution=(self.res_horizontal, self.res_vertical), framerate=self.framerate)
        camera.iso = self.iso
        time.sleep(2)
        self.shutter_speed = camera.exposure_speed
        self.exposure_mode = 'off'
        self.awb_mode = 'off'
        self.awb_gains = camera.awb_gains
        camera.close()
        self.lock_camera = False

    def shoot(self):
        camera = PiCamera(resolution=(self.res_horizontal, self.res_vertical), framerate=self.framerate)
        camera.iso = self.iso
        # time.sleep(2)
        # Now fix the values
        # self.camera.shutter_speed = self.camera.exposure_speed
        # self.camera.exposure_mode = 'off'
        # g = self.camera.awb_gains
        # self.camera.awb_mode = 'off'
        # self.camera.awb_gains = g

        camera.shutter_speed = self.shutter_speed
        camera.exposure_mode = self.exposure_mode
        camera.awb_mode = self.awb_mode
        camera.awb_gains = self.awb_gains
        ts = datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
        for i in range(self.num_shots_per_take):
            # print(self.pics_dir + 'image_' + str(i) + '_' + ts + '.jpg')
            filepath = "%simage_%s_%s.jpg" % (self.pics_dir, str(i), ts)
            self.logger.debug(filepath)
            camera.capture(filepath, format='jpeg', use_video_port=True)
        camera.close()
