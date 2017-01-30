import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from os import listdir
from os.path import isfile, join


class NetHandler:

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def send_per_email(self, source_dir, destination_email, subject, text=''):
        self.logger.log('Sending pics from %s to %s' % (source_dir, destination_email))

        msg = MIMEMultipart()
        msg['From'] = self.config['email']['source_email']
        msg['To'] = self.config['email']['destination_email']
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach(MIMEText(text))

        files = [f for f in listdir(source_dir) if isfile(join(source_dir, f))]

        for f in files or []:
            with open(join(source_dir, f), "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(join(source_dir, f))
                msg.attach(part)

        smtp = smtplib.SMTP(self.config['email']['smtp']['hostname'], self.config['email']['smtp']['port'])
        smtp.ehlo()
        if self.config['email']['smtp']['use_tls']:
            smtp.starttls()
        if self.config['email']['smtp']['use_login']:
            smtp.login(self.config['email']['smtp']['login'], self.config['email']['smtp']['password'])
        smtp.sendmail(self.config['email']['source_email'], self.config['email']['destination_email'], msg.as_string())
        smtp.close()
