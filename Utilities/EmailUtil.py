import imaplib
import email
from bs4 import BeautifulSoup
import logging
from contextlib import contextmanager


class EmailReader:
    def __init__(self, email_id, password, mailbox="INBOX"):
        self.email_id = email_id
        self.password = password
        self.mailbox = mailbox
        self.mail_server = None

    @contextmanager
    def connection(self):
        self.mail_server = imaplib.IMAP4_SSL("imap.gmail.com")
        try:
            self.mail_server.login(self.email_id, self.password)
            yield
        except Exception as err:
            logging.warning(f'Login failed: {err}')
            yield
        finally:
            if self.mail_server.state != 'LOGOUT':
                self.mail_server.logout()

    def search_emails(self, sender=None, to=None, subject=None, is_seen=0):
        self.mail_server.select(self.mailbox)
        search_criteria = []
        if is_seen:
            search_criteria.append('SEEN')
        else:
            search_criteria.append('UNSEEN')
        if sender:
            search_criteria.append(f'FROM "{sender}"')
        if to:
            search_criteria.append(f'TO "{to}"')
        if subject:
            search_criteria.append(f'SUBJECT "{subject}"')

        status, mails = self.mail_server.search(None, f'({" ".join(search_criteria)})')
        mail_ids = mails[0].split()
        return mail_ids

    def fetch_emails(self, mail_ids, extract_links=False, extract_text=False, extract_table=False,
                     check_attachments=False):
        results = {"links": [], "texts": [], "tables": [], "attachments": []}
        for mail_id in mail_ids:
            status, mail_contents = self.mail_server.fetch(mail_id, "(RFC822)")
            raw_mail_content = mail_contents[0][1]
            message = email.message_from_bytes(raw_mail_content)

            for message_part in message.walk():
                content_type = message_part.get_content_type()

                if content_type == "text/html":
                    message_body = message_part.get_payload(decode=True).decode()
                    soup = BeautifulSoup(message_body, 'html.parser')

                    if extract_links:
                        links_in_message = [link["href"] for link in soup.find_all('a', href=True)]
                        results["links"].extend(links_in_message)

                    if extract_text:
                        message_tag = soup.find('p')
                        if message_tag:
                            message_text = message_tag.get_text()
                            if message_text not in results["texts"]:
                                results["texts"].append(message_text)

                    if extract_table:
                        table = soup.find('table')
                        if table:
                            headers = [header.text.strip() for header in table.find_all('th')]
                            rows = table.find_all('tr')
                            table_data = []
                            for row in rows:
                                columns = row.find_all('td')
                                if len(columns) == len(headers):
                                    row_data = [col.text.strip() for col in columns]
                                    table_data.append(row_data)
                            results["tables"].append((headers, table_data))

                if check_attachments:
                    content_disposition = str(message_part.get("Content-Disposition"))
                    if "attachment" in content_disposition:
                        attachment_info = {
                            "filename": message_part.get_filename(),
                            "content_type": content_type,
                            "size": len(message_part.get_payload(decode=True))
                        }
                        results["attachments"].append(attachment_info)

        return results

    def read_emails(self, sender=None, to=None, subject=None, is_seen=0, extract_links=False, extract_text=False,
                    extract_table=False, check_attachments=False):
        with self.connection():
            if not self.mail_server or self.mail_server.state == 'LOGOUT':
                return {"links": [], "texts": [], "tables": [], "attachments": []}
            mail_ids = self.search_emails(sender, to, subject, is_seen)
            return self.fetch_emails(mail_ids, extract_links, extract_text, extract_table, check_attachments)


def gmail_verify(email_id, password, sender, to, subject, is_seen=0):
    try:
        email_reader = EmailReader(email_id, password)
        return email_reader.read_emails(sender, to, subject, is_seen, extract_links=True)
    except Exception as err:
        logging.warning(f'{err}')
        return []


email_reader = EmailReader("credftest@gmail.com", "exxo roos pemw lgxr")
# # # links = email_reader.read_emails("j1605@credflow.co", "credftest@gmail.com",
# # #                                  "J D Polymers34 - (from 1-Apr-2019)] Pending Payment Reminder - Krise International",
# # #                                  extract_links=True)
# content = email_reader.read_emails("j1605@credflow.co", "credftest@gmail.com",
#                                    "[J D Polymers34 - (from 1-Apr-2019)] Pending Payment Reminder - Flexi Flow Polymers LLP",
#                                    extract_text=True)
# table_data = email_reader.read_emails("j1605@credflow.co", "credftest@gmail.com",
#                                       "J D Polymers34 - (from 1-Apr-2019)] Pending Payment Reminder - Krise International",
#                                       extract_links=True,extract_text=True,
#                     extract_table=True, check_attachments=True)
# attachments = email_reader.read_emails("j1605@credflow.co", "credftest@gmail.com",
#                                        "[J D Polymers34 - (from 1-Apr-2017)] Pending Payment Reminder - Pooja Enterprises",
#                                        check_attachments=True)

# print("Links:", links["links"])
# print("Content:", content["texts"])
# print("Table Data:", table_data)
# print("Attachments:", attachments["attachments"])
