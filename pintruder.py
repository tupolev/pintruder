from os import listdir, unlink
from os.path import isdir, isfile, join
from gpiozero import MotionSensor
from yaml import load
from picamera.exc import PiCameraRuntimeError
import logging
from Camera import Camera
from NetHandler import NetHandler
from Logger import Logger


class Pintruder:

    def __init__(self, config, logging):
        self.config = config
        self.mail_text = 'Pintruder in Zerocam detected a potential intrusion'
        self.mail_subject = 'Potential intrusion detected'
        self.num_shots_per_take = self.config['camera']['num_shots_per_take']
        self.pic_temp_dir = self.config['pic_temp_dir']
        self.motion_detector_pin_number = self.config['motion_detector_pin_number']
        self.debug_enabled = self.config['debug']
        self.logger = Logger(self.config, logging)
        self.cam = Camera(self.config, self.logger)
        self.net = NetHandler(self.config['net'], self.logger)
        self.destination_email = self.config['net']['email']['destination_email']

    def shoot(self):
        self.logger.log('Shooting')
        self.cam.shoot()
        self.logger.debug('Shot')

    def send_pics(self):
        self.logger.log('Sending')
        self.net.send_per_email(self.config['pic_temp_dir'], self.destination_email, self.mail_subject, self.mail_text)
        self.logger.debug('Sent')

    def clean(self):
        pic_dir = self.config['pic_temp_dir']
        self.logger.log('cleaning %s' % pic_dir)
        if isdir(pic_dir):
            for f in listdir(pic_dir):
                if isfile(join(pic_dir, f)):
                    unlink(join(pic_dir, f))
        self.logger.debug('cleaned %s' % pic_dir)

    def main(self):
        self.logger.log('Pre cleaning output directory')
        self.clean()
        self.logger.log('Surveillance ON')
        pir = MotionSensor(self.config['motion_detector_pin_number'])
        while True:
            try:
                if pir.motion_detected and not self.cam.lock_camera:
                    self.shoot()
                    self.send_pics()
                    self.clean()
            except (KeyboardInterrupt, SystemExit):
                self.logger.log('User exit request detected. Ending program')
                exit()

try:
    with open('config.yml', 'r') as f:
        init_config = load(f)
    logging.basicConfig(
        filename=init_config['config']['debug']['log_path'],
        level=logging.DEBUG if init_config['config']['debug']['enabled'] else logging.WARNING
    )
    Pintruder(init_config['config'], logging).main()
except PiCameraRuntimeError as e:
    logging.error("Fatal error: %s" % str(e))
except Exception as e:
    logging.error("Fatal error: Cannot load configuration from file config.yml. Reason: %s" % str(e))
finally:
    exit()
