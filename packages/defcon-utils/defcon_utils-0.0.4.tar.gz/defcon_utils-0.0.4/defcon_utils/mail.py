from .exceptions import *

class MailApiHandler(object):
    DEFAULT_FROM_EMAIL = ""
    SENDGRID_API_KEY = None
    
    def __init__(self, from_address, sendgrid_api_key=None, mailgun_api_key=None):
        self.DEFAULT_FROM_EMAIL = from_address
        
        if sendgrid_api_key: 
            self.SENDGRID_API_KEY = sendgrid_api_key
            self.sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        elif mailgun_api_key: 
            self.MAILGUN_API_KEY = mailgun_api_key
        else: 
            raise InvalidLoginException


    @staticmethod
    def process_response(response):
        """
        Raises an exception if the response was not successful
        :param response: SendGrid client response
        :return: Body string of the response
        """
        status = response.status_code

        if not (200 <= status < 300):
            # The response was not successful
            raise MailNotSentException(response.text)

        return response

    def send_email_via_mailgun(self, to, subject, content, html_content, attachments):
        import requests
        files = []
        for attachment in attachments:
            data = attachment['data']
            if isinstance(data, str):
                data = data.encode()

            encoded_file = base64.b64encode(data).decode()
            files.append(("attachment", (attachment['file_name'], data)))

        return requests.post(
            "https://api.mailgun.net/v3/mg.anveshan.tech/messages",
            auth=("api", self.MAILGUN_API_KEY),
            files=files,
            data={"from": "Anveshan API <{}>".format(self.DEFAULT_FROM_EMAIL),
                  "to": to,
                  "subject": subject,
                  "text": content,
                  "html": html_content})

    def send_mail(self, to, subject, content=None, html_content=None, attachments=None):
        """
        Send a email using SendGrid
        :param to: <List:String> Email ids to which email needs to be sent
        :param subject:
        :param content:
        :param html_content:
        :param attachments: List of Dict: {"data": "", "file_name": {}, "file_type"}
        :return:
        """
        if not attachments:
            attachments = []
        response = None
        if self.MAILGUN_API_KEY: 
            response = self.send_email_via_mailgun(to, subject, content, html_content, attachments)
        elif self.SENDGRID_API_KEY: 
            message = Mail(
                from_email=self.DEFAULT_FROM_EMAIL,
                to_emails=to,
                subject=subject,
                plain_text_content=content,
                html_content=html_content)

            for attachment in attachments:
                data = attachment['data']
                if isinstance(data, str):
                    data = data.encode()

                encoded_file = base64.b64encode(data).decode()

                attachedFile = Attachment(
                    FileContent(encoded_file),
                    FileName(attachment['file_name']),
                    FileType(attachment['file_type']),
                    Disposition('attachment')
                )
                message.attachment = attachedFile

                response = self.sendgrid_client.send(message)

        self.process_response(response)
        
        return True
    

class ImapSmtpMailHandler(object):
    imap_connection = None
    smtp_connection = None
    file_name = None
    file_path = None
    mailbox = 'inbox'

    def __init__(self, username, password, file_name=None, file_path=None):
        self.username = username
        self.password = password

        self.file_name = file_name
        self.file_path = file_path

    def login_imap(self):
        self.imap_connection = imaplib.IMAP4_SSL("imap.googlemail.com", 993)
        self.imap_connection.login(self.username, self.password)

    def login_smtp(self):
        self.smtp_connection = smtplib.SMTP('smtp.gmail.com:587')
        self.smtp_connection.ehlo()
        self.smtp_connection.starttls()
        self.smtp_connection.login(self.username, self.password)

    def get_all_email_uids(self, search_criteria='ALL'):
        # For example search criteria checkout http://www.marshallsoft.com/ImapSearch.htm
        if not self.imap_connection:
            self.login_imap()
        self.imap_connection.select(self.mailbox)
        typ, msgs = self.imap_connection.search(None, search_criteria)
        msgs = msgs[0].split()
        return msgs

    def set_mailbox(self, mailbox):
        self.mailbox = mailbox

    def set_file_download_path(self, path):
        self.file_path = path

    def get_mail_object_from_uid(self, uid):
        if not self.imap_connection:
            self.login_imap()
        assert uid, "Cannot get mail object without UID"
        try:
            self.imap_connection.select(self.mailbox)
            resp, data = self.imap_connection.fetch(uid, '(RFC822)')
            email_body = data[0][1]
            return email.message_from_string(email_body)
        except Exception as e:
            raise NoMailObjectException

    @staticmethod
    def get_email_body_html_from_mail_object(msg):
        """
        Decode email body and get html text
        """
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))
                # skip any text/plain (txt) attachments
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    continue
                elif ctype == 'text/html':
                    body = part.get_payload(decode=True)  # decode
                    return body
        else:
            encoding = msg.get('Content-Transfer-Encoding')
            decode_flag = True if encoding and (encoding == 'base64' or encoding == 'quoted-printable') else False
            return msg.get_payload(decode=decode_flag)

    def download_attachment_from_mail_object(self, mail_object, file_path=None, file_name=None, skip_file_check=False):
        """
        Downloads the attachment to specified path with specified filename
        :param mail_object:
        :param file_path:
        :param file_name:
        :param skip_file_check: Bool, if True the file is over written and no exception is raised
        :return: Boolean (True for successful download, False if downlaod fails)
        """
        assert mail_object, "Cannot get attachment without mail object"
        if not self.imap_connection:
            self.login_imap()
        if mail_object.get_content_maintype() != 'multipart':
            return False
        if file_name:
            self.file_name = file_name
        if file_path:
            self.file_path = file_path
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
        for part in mail_object.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            if not self.file_name:
                self.file_name = part.get_filename()
            if self.file_name is not None:
                path = os.path.join(self.file_path, self.file_name)
                if not skip_file_check:
                    if os.path.isfile(path):
                        raise MailException("File already exists in the specified location")
                else:
                    fp = open(path, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
                    return True
        return False

    def send_mail(self, receivers, subject, body, files=[], reply_mail_id=None, sender=None):
        """
        Send a new email using smtp
        :param receivers: List of complete email ids to which email must be sent
        :param subject: Subject string of the email
        :param body: Email  body
        :param files: List of dict {"name" - file name, "data" - compelte data content to send}
        :param reply_mail_id: The UID (Message-Id) of the original email to which you wish to reply as thread. Note that
        the subject must be same for both the emails if you wish to show it as thread.
        :param sender: The email id of the sender
        :return: None
        """
        if not self.smtp_connection:
            self.login_smtp()
        assert receivers and subject, "Cannot send mail without receivers"
        if not sender:
            sender = self.username
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = ", ".join(receivers)
        msg['Subject'] = subject
        if reply_mail_id:
            msg['References'] = msg['In-Reply-To'] = reply_mail_id
        msg.attach(MIMEText(body))

        # Attach files
        for file in files:
            part = MIMEBase('application', 'octet-stream')
#             if os.path.isfile(file):
            part.set_payload(file["data"])
            encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"'
                            % file["name"])
            msg.attach(part)
#             else:
#                 raise BPMailException("Invalid file path for file: ", file)
        self.smtp_connection.sendmail(sender, receivers, msg.as_string())