import boto3
from config import Config


class EmailSender:

    def __init__(self):
        # SET CREDENTIALS
        config = Config.get_config()
        # print(config)
        self.client = boto3.client('ses',
                                   region_name='eu-west-2',
                                   aws_access_key_id=config['ACCESS_ID'],
                                   aws_secret_access_key=config['ACCESS_KEY']
                                   )
        self.to_address = config['EMAIL_TO']
        self.from_address = config['EMAIL_FROM']
        self.website = 'https://glastonbury.seetickets.com/content/extras'

    def send_email_action(self):
        subject = "ACTION REQUIRED: check glasto website"
        body = f"quick get on line to get glasto tickets: {self.website}"

        response = (self.client.send_email(
            Source=self.from_address,
            Destination={'ToAddresses': [self.to_address]},
            Message={'Subject': {'Data': subject},
                     'Body': {'Text': {'Data': body}}
                     }
        ))
        print(response)
        print('Tickets available email sent')

    def send_email_noaction(self):
        subject = "no news is bad news"
        body = f"still sold out: {self.website}"

        response = self.client.send_email(
            Source=self.from_address,
            Destination={'ToAddresses': [self.to_address]},
            Message={'Subject': {'Data': subject},
                     'Body': {'Text': {'Data': body}}
                     }
        )
        print(response)
        print('Sold out email sent')
