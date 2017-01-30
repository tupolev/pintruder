import logging


class Logger:
    def __init__(self, config, logging_module_instance):
        self.logging = logging_module_instance
        self.debug_enabled = config['debug']['enabled'] or False
        self.send_to_screen = config['debug']['send_to_screen'] or True
        self.send_to_file = config['debug']['send_to_file'] or True

    def log(self, message, level=logging.INFO):
        if self.send_to_file:
            self.logging.log(level, message)
        if self.send_to_screen:
            print(message)

    def debug(self, message):
        if self.debug_enabled:
            self.log(message, self.logging.DEBUG)
