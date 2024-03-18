import imaplib
import email
from bs4 import BeautifulSoup
import logging


# import sys, pdb

def extract_links_from_message(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    linksinMessage = []
    for link in soup.find_all('a', href=True):
        # absolute_link = urljoin(base_url, link['href'])
        absolute_link = link["href"]
        # pdb.Pdb(stdout=sys.__stdout__).set_trace()
        linksinMessage.append(absolute_link)
    return linksinMessage


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


def gmail_verify(emailId, password, senderMail, to, subject, isSeen=0):
    try:
        allLinks = read_unread_emails(emailId, password, senderMail, to, subject, isSeen)
        # pdb.Pdb(stdout=sys.__stdout__).set_trace()
        return allLinks
    except Exception as err:
        # pdb.Pdb(stdout=sys.__stdout__).set_trace()
        logging.warning(f'{err}')
        return []


