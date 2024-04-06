import boto3
import json
import requests
import datetime
from bs4 import BeautifulSoup


def lambda_handler(event, context):

    now = datetime.datetime.now()
    print(f"LOGGING: lambda START at: {now}")

    website = 'https://glastonbury.seetickets.com/content/extras'
    r = requests.get(website)
    soup = BeautifulSoup(r.content, 'html.parser')

    finder_status = True
    search_phrase = 'balance'
    xs = soup.find_all('p')
    for idx, content in enumerate(xs):
        if search_phrase in str(content):
            break
        else:
            finder_status = False

    now = datetime.datetime.now()

    if finder_status:
        print(f"LOGGING: {now} | keyword: '{search_phrase}' found on site")
        subject = "no news is bad news"
        body = f"still sold out: {website}"
        send_email(subject, body)
        send_text(f"{subject} {body}")
    else:
        print(f"LOGGING: {now} | keyword: '{search_phrase}' NOT found on site .... send warning text message")
        subject = "ACTION REQUIRED: check glasto website"
        body = f"quick get on line to get glasto tickets: {website}"
        send_email(subject, body)
        send_text(f"{subject} {body}")

    now = datetime.datetime.now()
    print(f"LOGGING: lambda END at: {now}")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def send_email(subject, body):
    print('LOGGING: Sending EMAIL process START')
    client = boto3.client('ses')
    to_address = 'andyjcarter77@gmail.com'
    from_address = 'andy@thepubcrawls.co.uk'

    response = client.send_email(
        Source=from_address,
        Destination={'ToAddresses': [to_address]},
        Message={'Subject': {'Data': subject},
                 'Body': {'Text': {'Data': body}}
                 }
    )
    print(f'LOGGING: {response}')
    print(f'LOGGING: {subject} email sent')
    print('LOGGING: Sending EMAIL process END')


def send_text(msg):
    print('LOGGING: Sending TEXT process START')
    contact_tel = '+447507777568'
    client = boto3.client('sns')
    response = client.publish(PhoneNumber=contact_tel,
                   Message=msg,
                   MessageAttributes={
                        'AWS.SNS.SMS.SenderID': {
                            'DataType': 'String',
                            'StringValue': 'GlastoAlert'
                        }}
                   )
    print(f'LOGGING: {response}')
    print(f'LOGGING: {msg} text sent')
    print('LOGGING: Sending TEXT process END')
