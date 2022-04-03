import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config


def send_mail(receiver_name, receiver_address, link):
    sender_email = config("EMAIL_ADDRESS")
    receiver_email = receiver_address
    password = config("EMAIL_PWD")
    name = receiver_name

    message = MIMEMultipart("alternative")
    message["Subject"] = "Fynd Academy Enrollment Fees"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = f"""\
    Hi {name},
    Hope you are doing well. To confirm your admission in Fynd academy you will have to pay enrollment fees Rs. 500.
    Kindly make the payment using the below link.
    """
    html = f"""\
    <html>
      <body>
        <p>Hi {name},</p><br>
      <p>Hope you are doing well.To confirm your admission in Fynd academy you will have to pay enrollment fees Rs. 500.
    Kindly make the payment using the below link.</p><br>
        <p>Proceed for payment<br>
           <a href={link}>click on this link</a>
        </p>
        <img src="https://assets.website-files.com/603683469df97967298e6e81/6037ed523cde7f1958341705_logo-p-500.png"
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )



# import smtplib
# import config
#
# amount = 500
# toaddrs = "sid007trading@gmail.com"
#
# def send_mail():
#     try:
#         server = smtplib.SMTP('smtp.gmail.com:587')
#         server.ehlo()
#         server.starttls()
#         server.login(config.EMAIL_ADDRESS, config.EMAIL_PWD)
#         message = f"""From: {config.EMAIL_ADDRESS}\r
#         \r
#         Pay {amount} bitcoin or else. We're watching.\r
#         """

