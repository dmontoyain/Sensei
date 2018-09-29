import smtplib

from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# This function grabs the letter template from the filename and returns a template object

MY_ADDRESS = GIVE AN EMAIL
PASSWORD = GIVE THE PASSWORD

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def sendSenseiNotification(mentorLogin, studentLogin, projectName):
    print(mentorLogin)
    message_template = read_template('template.txt')

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com:587')
    s.ehlo()
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    # For each contact, send the email:
    msg = MIMEMultipart()       # create a message

    # add in the actual person name to the message template
    message = message_template.substitute(MENTOR_LOGIN=mentorLogin,STUDENT_LOGIN=studentLogin,PROJECT=projectName)

    # Prints out the message body for our sake
    print(message)

    # setup the parameters of the message
    msg['From']=MY_ADDRESS
    msg['To']=mentorLogin + "@student.42.us.org"
    msg['Subject']="Sensei Appointment"

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg

    # Terminate the SMTP session and close the connection
    s.quit()

sendSenseiNotification("bpierce", "kmckee", "Ogres Having Layers")
