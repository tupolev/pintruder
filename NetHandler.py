import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from os import listdir
from os.path import isfile, join


class NetHandler:

    def __init__(self, config):
        self.config = config

    def send_per_email(self, source_dir, destination_email, subject, text=''):
        print('sending pics from ', source_dir, ' to ', destination_email)

        msg = MIMEMultipart()
        msg['From'] = self.config['source_email']
        msg['To'] = self.config['destination_email']
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

        smtp = smtplib.SMTP(self.config['smtp']['hostname'], self.config['smtp']['port'])
        smtp.ehlo()
        if self.config['smtp']['use_tls']:
            smtp.starttls()
        if self.config['smtp']['use_login']:
            smtp.login(self.config['smtp']['login'], self.config['smtp']['password'])
        smtp.sendmail(self.config['source_email'], self.config['destination_email'], msg.as_string())
        smtp.close()
