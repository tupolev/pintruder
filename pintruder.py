from os import listdir, unlink
from os.path import isdir, isfile, join
from gpiozero import MotionSensor
from yaml import load

from Camera import Camera
from NetHandler import NetHandler


class Pintruder:

    def __init__(self, config):
        self.config = config['config']
        self.mail_text = 'Pintruder in Zerocam detected a potential intrusion'
        self.mail_subject = 'Potential intrusion detected'
        self.num_shots_per_take = self.config['camera']['num_shots_per_take']
        self.pic_temp_dir = self.config['pic_temp_dir']
        self.motion_detector_pin_number = self.config['motion_detector_pin_number']
        self.cam = Camera(self.config['camera'])
        self.net = NetHandler(self.config['net']['email'])
        self.destination_email = self.config['net']['email']['destination_email']

    def shoot(self):
        print('shooting')
        self.cam.shoot(self.config['camera']['num_shots_per_take'], self.config['pic_temp_dir'])
        print('shot')

    def send_pics(self):
        print('sending')
        self.net.send_per_email(self.config['pic_temp_dir'], self.destination_email, self.mail_subject, self.mail_text)
        print('sent')

    def clean(self):
        pic_dir = self.config['pic_temp_dir']
        print('cleaning ', pic_dir)
        if isdir(pic_dir):
            for f in listdir(pic_dir):
                if isfile(join(pic_dir, f)):
                    unlink(join(pic_dir, f))
        print('cleaned ', pic_dir)

    def main(self):
        print('Pre cleaning output directory')
        self.clean()
        print('Surveillance ON')
        pir = MotionSensor(self.config['motion_detector_pin_number'])
        while True:
            try:
                if pir.motion_detected:
                    self.shoot()
                    self.send_pics()
                    self.clean()
            except (KeyboardInterrupt, SystemExit):
                print('User exit request detected. Ending program')
                exit()

try:
    with open('config.yml', 'r') as f:
        init_config = load(f)

except Exception as e:
    print('Fatal error: Cannot load configuration from file config.yml. Reason: ', e)
    exit()

Pintruder(init_config).main()
