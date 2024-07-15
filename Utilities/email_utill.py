import imaplib
import email
from bs4 import BeautifulSoup
import logging


def extract_links_from_message(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    linksinMessage = []
    for link in soup.find_all('a', href=True):
        # absolute_link = urljoin(base_url, link['href'])
        absolute_link = link["href"]
        # pdb.Pdb(stdout=sys.__stdout__).set_trace()
        linksinMessage.append(absolute_link)
    return linksinMessage


def extract_text_from_message_body(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    message_tag = soup.find('p')
    if message_tag:
        extracted_text = message_tag.get_text()
        return extracted_text


def extract_table_from_message_body(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')  # Assuming there's only one table in the email body
    table_data = []

    if table:
        headers = [header.text.strip() for header in table.find_all('th')]
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) == len(headers):
                row_data = [col.text.strip() for col in columns]
                table_data.append(row_data)

    return headers, table_data


def read_unread_emails(emailId, password, senderMail=None, to=None, subject=None, isSeen=0, mailbox="INBOX"):
    mailServer = imaplib.IMAP4_SSL("imap.gmail.com")
    mailServer.login(emailId, password)
    mailServer.select(mailbox)
    search_criteria = ''
    if isSeen:
        search_criteria += f'SEEN '
    else:
        search_criteria += f'UNSEEN '
    if senderMail:
        search_criteria += f'FROM "{senderMail}" '
    if to:
        search_criteria += f'TO "{to}" '
    if subject:
        search_criteria += f'SUBJECT "{subject}"'
    status, mails = mailServer.search(None, f'({search_criteria})')
    mails = mails[0].split()
    allLinks = []
    for mail in mails:
        status, mailContents = mailServer.fetch(mail, "(RFC822)")
        rawMailContent = mailContents[0][1]
        message = email.message_from_bytes(rawMailContent)

        for messagePart in message.walk():
            contentType = messagePart.get_content_type()
            content_disposition = str(messagePart.get("Content-Disposition"))
            if contentType == "text/html":
                messageBody = messagePart.get_payload(decode=True).decode()
                linksInMessage = extract_links_from_message(messageBody, base_url=message.get("From"))
                allLinks.extend(linksInMessage)
    mailServer.logout()
    return allLinks


def read_email_content(emailId, password, senderMail=None, to=None, subject=None, isSeen=0, mailbox="INBOX"):
    mailServer = imaplib.IMAP4_SSL("imap.gmail.com")
    mailServer.login(emailId, password)
    mailServer.select(mailbox)
    search_criteria = ''
    if isSeen:
        search_criteria += f'SEEN '
    else:
        search_criteria += f'UNSEEN '
    if senderMail:
        search_criteria += f'FROM "{senderMail}" '
    if to:
        search_criteria += f'TO "{to}" '
    if subject:
        search_criteria += f'SUBJECT "{subject}"'
    status, mails = mailServer.search(None, f'({search_criteria})')
    mails = mails[0].split()
    msg = []
    for mail in mails:
        status, mailContents = mailServer.fetch(mail, "(RFC822)")
        rawMailContent = mailContents[0][1]
        message = email.message_from_bytes(rawMailContent)
        for messagePart in message.walk():
            contentType = messagePart.get_content_type()
            content_disposition = str(messagePart.get("Content-Disposition"))
            if contentType == "text/html":
                messageBody = messagePart.get_payload(decode=True).decode()
                messageText = extract_text_from_message_body(messageBody)
                if messageText not in msg:  # Check if message text is already added
                    msg.append(messageText)
    mailServer.logout()
    return msg


def read_email_table_content(emailId, password, senderMail=None, to=None, subject=None, isSeen=0, mailbox="INBOX"):
    mailServer = imaplib.IMAP4_SSL("imap.gmail.com")
    mailServer.login(emailId, password)
    mailServer.select(mailbox)
    search_criteria = ''
    if isSeen:
        search_criteria += f'SEEN '
    else:
        search_criteria += f'UNSEEN '
    if senderMail:
        search_criteria += f'FROM "{senderMail}" '
    if to:
        search_criteria += f'TO "{to}" '
    if subject:
        search_criteria += f'SUBJECT "{subject}"'
    status, mails = mailServer.search(None, f'({search_criteria})')
    mails = mails[0].split()
    msg = []
    for mail in mails:
        status, mailContents = mailServer.fetch(mail, "(RFC822)")
        rawMailContent = mailContents[0][1]
        message = email.message_from_bytes(rawMailContent)
        for messagePart in message.walk():
            contentType = messagePart.get_content_type()
            if contentType == "text/html":
                messageBody = messagePart.get_payload(decode=True).decode()
                headers, table_data = extract_table_from_message_body(messageBody)
                msg.append((headers, table_data))
    mailServer.logout()
    return msg


def gmail_verify(emailId, password, senderMail, to, subject, isSeen=0):
    try:
        allLinks = read_unread_emails(emailId, password, senderMail, to, subject, isSeen)
        # pdb.Pdb(stdout=sys.__stdout__).set_trace()
        return allLinks
    except Exception as err:
        # pdb.Pdb(stdout=sys.__stdout__).set_trace()
        logging.warning(f'{err}')
        return []


links = gmail_verify("credftest@gmail.com", "exxo roos pemw lgxr", "j1605@credflow.co",
                     "credftest@gmail.com",
                     "J D Polymers34 - (from 1-Apr-2019)] Pending Payment Reminder - Krise International")
content = read_email_content("credftest@gmail.com", "exxo roos pemw lgxr", "j1605@credflow.co",
                             "credftest@gmail.com",
                             "J D Polymers34 - (from 1-Apr-2019)] Pending Payment Reminder - Krise International")
table_data = read_email_table_content("credftest@gmail.com", "exxo roos pemw lgxr", "j1605@credflow.co",
                                      "credftest@gmail.com",
                                      "J D Polymers34 - (from 1-Apr-2019)] Pending Payment Reminder - Krise International")
print(content)
