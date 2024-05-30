from Google import Create_Service
from langdetect import detect
from googletrans import Translator
import pickle

CLIENT_FILE = 'JsonFile/dtclient.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']
service = Create_Service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)

with open('model/spam_email.sav', 'rb') as model_file:
    loaded_model, loaded_extractor = pickle.load(model_file)

def mark_as_read(message_id):
    try:
        service.users().messages().modify(userId='me', id=message_id, body={'removeLabelIds': ['UNREAD']}).execute()
    except Exception as error:
        print(f"Xuất hiện lỗi: {error}")
def mark_as_spam(message_id):
    try:
        service.users().messages().modify(userId="me", id=message_id, body={'removeLabelIds': [], 'addLabelIds': ['SPAM']}).execute()
    except Exception as error:
        print(f"Xuất hiện lỗi: {error}")

def mark_as_inbox(message_id):
    try:
        service.users().messages().modify(userId='me', id=message_id, body={'addLabelIds': ['INBOX'], 'removeLabelIds': ['SPAM']}).execute()
    except Exception as error:
        print(f"Xuất hiện lỗi: {error}")

def detect_and_translate(text):
    if detect(text) != 'en':
        translator = Translator()
        translated = translator.translate(text, dest='en')
        return translated.text
    else:
        return text

def predict_email(mail):
    translated_mail = detect_and_translate(mail)
    processed = loaded_extractor.transform([translated_mail])
    predicted = loaded_model.predict(processed)
    return str(predicted[0])


