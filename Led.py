from gpiozero import LED


class Led:
    def __init__(self, gpio_main_led_pin, logger):
        self.logger = logger
        self.led = LED(gpio_main_led_pin)
        self.led_is_on = self.led.is_active
        self.logger.log('LED initialized and set off')

    def toggle(self):
        self.led.toggle()
        self.led_is_on = self.led.is_active
        self.logger.debug('Toggle LED to %s' % self.led.is_active)

    def get_status(self):
        return self.led_is_on

    def on(self):
        self.led.on()
        self.led_is_on = self.led.is_active
        self.logger.debug('LED turned on')

    def off(self):
        self.led.off()
        self.led_is_on = self.led.is_active
        self.logger.debug('LED turned off')
