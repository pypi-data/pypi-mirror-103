# -*- coding:utf-8 -*-
#!/usr/bin/env python

import sys
import os
import re

from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

from src.setting import USERNAME, PASSWORD

class AliyunEmail():

    def __init__(self, destination : list = None, subject : str = "Sent from Python"):

        self.msg = MIMEMultipart()

        self.SMTPserver = "smtp.mxhichina.com"
        self.sender = "yanghua@fenxianglife.com"

        if destination is None:
            self.destination = ["yanghua@fenxianglife.com"]
        elif isinstance(destination,list) == True:
            self.destination = destination
        else:
            sys.exit("type of destination is wrong")

        self.subject = subject

        self.msg["Subject"] = self.subject
        self.msg["From"] = self.sender  # some SMTP servers will do this automatically, not all


    def send_email(self,text_content : str = "Test", text_subtype : str = "plain"):
        try:
            # text content
            msg_text = MIMEText(text_content, text_subtype)
            self.msg.attach(msg_text)

            # attchment
            msg_application = MIMEApplication(open("C:/Users/YangHua/Desktop/每天数据-终.xlsx", "rb").read())
            msg_application.add_header("Content-Disposition", "attachment", filename= "test.csv")
            self.msg.attach(msg_application)

            conn = SMTP(self.SMTPserver)
            conn.set_debuglevel(True)
            conn.login(USERNAME, PASSWORD)
            try:
                conn.sendmail(self.sender, self.destination, self.msg.as_string())
            finally:
                conn.quit()

        except:
            sys.exit( "mail failed; %s" % "CUSTOM_ERROR" ) # give an error message

        
if __name__ == "__main__":
    AliyunEmail().send_email()