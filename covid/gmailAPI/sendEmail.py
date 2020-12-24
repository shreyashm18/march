from .Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
from email.mime.image import MIMEImage
import os


class send_email:
    def __init__(self,service):
        self.service = service
    
    def create_message_with_attachment(self,
        sender, to, subject, message_text, file):
      message = MIMEMultipart()
      message['to'] = to
      message['from'] = sender
      message['subject'] = subject

      msg = MIMEText(message_text)
      message.attach(msg)

      content_type, encoding = mimetypes.guess_type(file)

      if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
      main_type, sub_type = content_type.split('/', 1)
      if main_type == 'text':
        fp = open(file, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
      elif main_type == 'image':
        fp = open(file, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
      else:
        fp = open(file, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
      filename = os.path.basename(file)
      msg.add_header('Content-Disposition', 'attachment', filename=filename)
      message.attach(msg)

      return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    def send_message(self, user_id, message):
      try:
        message = (self.service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print(f"Message Id: {message['id']}")
        return message
      except errors.HttpError as error:
        print(f"An error occurred: {error}")
def connect_method(mail_id,pic_location):
  CLIENT_SECRET_FILE = 'D:/interview/task/covid/gmailAPI/credentials.json'
  API_NAME = 'gmail'
  API_VERSION = 'v1'
  SCOPES = ['https://mail.google.com/']

  service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
  sendObj = send_email(service=service)
  message = sendObj.create_message_with_attachment('me',mail_id,'COVID DATA BAR CHART','Please find below Bar Chart of COVID report', pic_location)
  sendObj.send_message('me',message)