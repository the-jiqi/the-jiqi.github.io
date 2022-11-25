import imaplib
import email
from email.header import decode_header
import webbrowser
import os

# account credentials
username = ""
password = ""

imap_server = "outlook.office365.com"


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)


# create an IMAP4 class with SSL
imap = imaplib.IMAP4_SSL(imap_server)
# authenticate
imap.login(username, password)

status, messages = imap.select("INBOX")
# number of top emails to fetch
N = 2
# total number of emails
messages = int(messages[0])

storage_list = []
items_list = []
for x in range(N):
    storage_list.append([])

for i in range(messages, messages - N, -1):
    # fetch the email message by ID
    res, msg = imap.fetch(str(i), "(RFC822)")

    for response in msg:
        if isinstance(response, tuple):
            # parse a bytes email into a message object
            msg = email.message_from_bytes(response[1])
            # decode the email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                # if it's a bytes, decode to str
                subject = subject.decode(encoding)
            # decode email sender
            From, encoding = decode_header(msg.get("From"))[0]
            if isinstance(From, bytes):
                From = From.decode(encoding)

            # checking to make sure email is from the right sender
            if From == 'Jotform':

                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts

                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass

                        # prints the main body text of the email
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # print text/plain emails and skip attachments
                            text = body.replace("\xa0", "").replace("\r", "").replace("\n", "")
                            # text = text[slice(0,len(text)-66)]
                            storage_list[i - 3].append(subject[4:])
                            storage_list[i - 3].append(text[18:29])
                            temp = text[29:].split(",,")
                            storage_list[i - 3].append(temp[0])
                            storage_list[i - 3].append(temp[1][7:])

# close the connection and logout
imap.close()
imap.logout()

for order in storage_list:
    print(f"{order[0]}\n{order[1]}:\n{order[2]}\n\n{order[3]}")
    print("=-" * 100)
