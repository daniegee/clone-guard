import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime

class EmailSender:
    def __init__(self, source_email, source_password, destination_email):
        self.source = source_email
        self.password = source_password
        self.destination = destination_email
        self.smtp_server = 'smtp.gmail.com'
        self.port = 587

    def send_email(self, image_path, card_uid):
        subject = 'ALERT: Building Access Attempt'
        
        # Styled HTML message body
        message_body = f'''
        <html>
        <body>
          <h2 style="color: red;">ALERT: Invalid Access Attempt!</h2>
          <p><strong>Building:</strong></p>
          <p><strong>Occurred at:</strong> {datetime.datetime.now()}</p>
          <p><strong>Scanned Card UID:</strong> {card_uid}</p>
          <p>Please see the attached image for further details.</p>
          <br/>
          <p style="color: grey; font-size: 12px;">This is an automated message. Please do not reply.</p>
        </body>
        </html>
        '''

        # Set up the email message
        message = MIMEMultipart()
        message['From'] = self.source
        message['To'] = self.destination
        message['Subject'] = subject
        message.attach(MIMEText(message_body, 'html'))

        # Open the image file in binary mode
        with open(image_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header with the image filename
        part.add_header('Content-Disposition', f'attachment; filename={image_path}')
        
        # Attach image
        message.attach(part)

        # Send the email
        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()  # Enable security
                server.login(self.source, self.password)  # Login with the sender's email and password
                server.sendmail(self.source, self.destination, message.as_string())
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email. Error: {e}")
