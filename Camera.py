from datetime import datetime
import time
from picamera import PiCamera


class Camera:
    def __init__(self, config):
        self.res_horizontal = config['resolution_horizontal'] or 1280
        self.res_vertical = config['resolution_vertical'] or 720
        self.framerate = config['framerate'] or 30
        self.iso = config['iso'] or 600
        self.camera = None
        print('Initializing camera module')

    def shoot(self, num_shots, pics_dir):
        self.camera = PiCamera(resolution=(self.res_horizontal, self.res_vertical), framerate=self.framerate)
        self.camera.iso = self.iso
        time.sleep(2)
        # Now fix the values
        self.camera.shutter_speed = self.camera.exposure_speed
        self.camera.exposure_mode = 'off'
        g = self.camera.awb_gains
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = g
        timestamp = datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
        for i in range(num_shots):
            print(pics_dir + 'image_' + str(i) + '_' + timestamp + '.jpg')
            self.camera.capture(
                pics_dir + 'image_' + str(i) + '_' + timestamp + '.jpg',
                format='jpeg',
                use_video_port=True
            )
        self.camera.close()
