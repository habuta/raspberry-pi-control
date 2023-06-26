from twilio.rest import Client

# Twilio account SID and auth token


class Message:
    def __init__(self):
        account_sid = "AC697800ca16cc2e60885dae60b39311a3"
        auth_token = "8fda756a2115ce154055fead1f9cdd76"

        # Twilio phone number and recipient phone number
        self.twilio_number = '+14176092345'  
        self.recipient_number = '+251936726259'
        # Create a Twilio client
        self.client = Client(account_sid, auth_token)

    def send_message(self, body):
        # Send an SMS message
        message = self.client.messages.create(
            body=body,
            from_=self.twilio_number,
            to=self.recipient_number
        )

        # Print the message SID
        print("Message SID:", message.sid)

mes = Message()

send_message = mes.send_message