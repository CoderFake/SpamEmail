from flask import Flask
import ReadEmail
from ReadEmail import predict_email, mark_as_spam, mark_as_inbox, mark_as_read
import time

service = ReadEmail.service
# app = Flask(__name__)
#
#
# @app.route('/', methods=['POST'])
# def webhook():
#     request = {
#         'labelIds': ['INBOX'],
#         'topicName': 'projects/focus-antler-405317/topics/pub',
#         'labelFilterBehavior': 'INCLUDE'
#     }
#     ReadEmail.service.users().watch(userId='me', body=request).execute()
#     service = ReadEmail.service
#     query = 'is:unread'
#     results = service.users().messages().list(userId='me', q=query).execute()
#     messages = results.get('messages', [])
#     if messages:
#         for message in messages:
#             msg = service.users().messages().get(userId='me', id=message['id']).execute()
#             result = predict_email(str(msg['snippet']))
#         if result == "1":
#             mark_as_spam(msg['id'])
#         else:
#             mark_as_inbox(msg['id'])
#     ReadEmail.service.users().stop(userId='me').execute()
#     return 'OK', 200

def get_unread_emails_in_spam():
    try:
        results = service.users().messages().list(userId='me', q='in:spam is:unread').execute()
        messages = results.get('messages', [])
        if messages:
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                mark_as_inbox(msg['id'])
    except Exception as error:
        print(f"Xuất hiện lỗi: {error}")

def get_unread_email():
    try:
        results = service.users().messages().list(userId='me', q='is:unread').execute()
        messages = results.get('messages', [])
        if messages:
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                result = predict_email(str(msg['snippet']))
                if result == "1":
                    mark_as_read(msg['id'])
                    mark_as_spam(msg['id'])
        else:
            print("Tất cả tin nhắn đã được đọc!")
    except Exception as error:
        print(f"Xuất hiện lỗi: {error}")


if __name__ == '__main__':
    get_unread_emails_in_spam()
    get_unread_email()








