import imaplib
import smtplib


class LIST:
    ALL = 'ALL'
    SENT = 'SENT'
    SPAM = 'SPAM'
    TRASH = 'TRASH'
    DRAFTS = 'DRAFTS'
    UNSEEN = 'UNSEEN'
    FLAGGED = 'FLAGGED'
    IMPORTANT = 'IMPORTANT'


class BOX:
    SENT = 'SENT'
    SPAM = 'SPAM'
    TRASH = 'TRASH'
    INBOX = 'INBOX'
    DRAFTS = 'DRAFTS'
    OUTBOX = 'OUTBOX'
    ARCHIVE = 'ARCHIVE'


# Define the account settings
username = ''
password = ''
server = ''
name = ''
imap_port = 993
smtp_port = 465

# Connect to IMAP server
mail = imaplib.IMAP4_SSL(server, imap_port)
mail.login(username, password)

# Select the INBOX folder
mail.select()

# Search for unread messages
status, messages = mail.search(None, LIST.ALL)
if not messages[0]:
    print("No unread messages found.")
else:
    messages = [int(msg) for msg in messages[0].split()]

    # Get the latest message (assuming it's the only one)
    message_id = messages[1]

    # Fetch the entire message
    raw_message_content, data = mail.fetch(str(message_id), '(RFC822)')
    raw_message_content = data[0][1]

    _to = ""
    for line in raw_message_content.decode().split('\n'):
        if line.startswith('From: '):
            _to = line[6:].strip()
            break

    if len(_to) > 0:

        subject = '''Test'''
        _from = f'{name} <{username}>'
        content = '''This is a test e-mail.'''
        raw = f'''From: {name} <{username}>\nTo: {_to}\nSubject: {subject}\n\n{content}'''

        server = smtplib.SMTP_SSL(server, smtp_port)
        server.login(username, password)
        server.sendmail(_from, _to, raw)
        server.quit()
