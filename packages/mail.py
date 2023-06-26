import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(message, video_file, subject="Alert"):
    # Email details
    sender_email = 'techlab.leul@gmail.com'
    sender_password = 'wajnmktcvnmvcpkc'
    recipient_email = 'yohannesmelese4@gmail.com'

    # Video file details

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Add the message body
    msg.attach(MIMEText(message, 'plain'))

    # Open the video file in binary mode
    with open(video_file, 'rb') as f:
        # Create a MIME base object
        video_part = MIMEBase('application', 'octet-stream')
        video_part.set_payload(f.read())

    # Encode the video file
    encoders.encode_base64(video_part)
    video_part.add_header('Content-Disposition', f'attachment; filename={video_file}')

    # Add the video attachment to the email
    msg.attach(video_part)

    try:
        # Create a secure connection with the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print('Email sent successfully!')

    except Exception as e:
        print('An error occurred while sending the email:', str(e))

    finally:
        # Close the SMTP connection
        server.quit()
