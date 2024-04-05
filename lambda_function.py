import boto3
import json
import requests
import datetime

from bs4 import BeautifulSoup

from config import Config
from mail_sender import EmailSender
from text_sender import TextSender


# def lambda_handler(event, context):
if __name__ == '__main__':
    # TODO implement
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }
    
    r = requests.get('https://glastonbury.seetickets.com/content/extras')
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
        print(f"{now} | keyword: '{search_phrase}' found on site")
        EmailSender().send_email_noaction()
    else:
        config = Config.get_config()
        print(f"{now} | keyword: '{search_phrase}' NOT found on site .... send warning text message")
        TextSender.send_text(config)
        EmailSender().send_email_action()
