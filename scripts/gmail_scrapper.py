import smtplib
import time
import imaplib
import email

in_server = "imap.gmail.com"
out_server = "smtp.gmail.com"
smtp_port = 993


class Scrapper(object):

    def get_emails(self, email_address, email_pwd):
        try:
            mail = imaplib.IMAP4_SSL(in_server)
            mail.login(email_address, email_pwd)
            mail.select("inbox")
            kind, data = mail.search(None, 'ALL')
            mail_ids = data[0].split()

            for _id in mail_ids:
                try:
                    mail_type, mail_data = mail.fetch(_id, '(RFC822)')
                    raw_email_string = mail_data[0][1].decode('utf-8')
                    message = email.message_from_string(raw_email_string)
                    for part in message.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True)
                    yield self.remove_sig(body)
                except Exception as e:
                    continue

        except Exception as e:
            print("Error retrieving emails: " + str(e))

    def remove_sig(self, text):
        try:
            i = text.find("You received this message because you are subscribed to the Google Groups")
            return text[:i]
        except Exception as e:
            return text
