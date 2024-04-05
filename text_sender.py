import boto3


class TextSender:

    @staticmethod
    def send_text(config):
        # SET CREDENTIALS
        sns = boto3.client('sns',
                           region_name='eu-west-2',
                           aws_access_key_id=config['ACCESS_ID'],
                           aws_secret_access_key=config['ACCESS_KEY']
                           )
        # SEND TEXT MSG
        sns.publish(PhoneNumber=config['CONTACT_TEL'],
                    Message='check website: https://glastonbury.seetickets.com/content/extras',
                    MessageAttributes={
                        'AWS.SNS.SMS.SenderID': {
                            'DataType': 'String',
                            'StringValue': 'GlastoAlert'
                        }}
                    )
