from django.core.mail import send_mail, EmailMessage
from django.db.models import Q
from datetime import datetime

ITMS_HEADER = "[ITMS]"


class ITMS_MSG:
    def __str__(self):
        return f"Email List:{self.email_list}"

    def __init__(self, host="", title=""):
        """__init__

        Args:
            host: server host ip / host name
            msg_type: Only users in this type will get notifications // Assigned by admin
        """
        self.host = host
        self.title = title
        self.bcc_list = ["xuefan.wang@fii-usa.com"]
        self.content_prefix = f"[TEST_ENV] {host}\n"
        self.title_prefix = f"[TEST_ENV] {ITMS_HEADER}"

    def build_content(self, msg_function, *args, **kwargs):
        """build_content

        Args:
            msg_function: the function that used to build messages

        Returns:
            msg_content: the message in html format
        """
        content = msg_function(*args, **kwargs, host=self.host)
        self.content = wrap_email(content)

    def set_email(self, email_list):
        self.email_list = email_list

    def send(self):
        """send msg

        Args:
            title: Email subject
            content: Email and Teams MSG content
        """
        msg = self.content_prefix + self.content
        subject = self.title_prefix + self.title
        send_celery_email(subject, msg, self.email_list, self.bcc_list)


# @shared_task
def send_celery_email(title=None, content=None, to_list=None, bcc_list=None, attachments=None):
    """send celery email

    Args:
        to_list: Receiver list.
        title: Email title.
        content: Builded html content / plain text.
        cc_list: CC list of Email.
        attachments: list of dictionaries.
            example:
            {
                "content": <class 'bytes'>,
                "content_filetype": "pdf",
                "filename": "example.pdf"
            }
    """
    email_ref = EmailMessage(
        subject=title,
        body=content,
        from_email="cims@fii-corp.com",
        to=to_list,
        bcc=bcc_list,
    )

    # if attachments:
    #     for attachment in attachments:
    #         part = MIMEApplication(attachment["content"], _subtype=attachment["content_filetype"])
    #         part.add_header("Content-Disposition", "attachment", filename=attachment["filename"])
    #         l6_email.attach(part)

    if email_ref:
        email_ref.content_subtype = "html"
        email_ref.send()


def wrap_email(content, host=""):
    return f"""
    <body style='font-family: "Segoe UI", "Helvetica", "sans-serif"'>
        <p>Hi, Team, </p>
        {content}
        <p>Sincerely</p>
        <p>ITMS group of CIMS Team FII Wisconsin</p>
        <h5><i>This is an automatic email sent from CIMS. </i></h5>
        <h5><i>This email is not monitored. Do not reply. </i></h5>
    </body>
    """


def new_account_content(emp_ref, acc_type_set, host):
    msg = f"""
        The following accounts of employee {emp_ref.employee_id}: {emp_ref.name} need to be created: <br><br>
        <table>
            <tr>
                <th>Account Type</th>
                <th>Person in Charge</th>
                <th>Action</th>
            </tr>
            
    """
    for acc_type in acc_type_set:
        msg += f"""
            <tr>
                <td>{acc_type.account_type}</td>
                <td>{acc_type.person_in_charge}</td>
                <td><a href="http://{host}/account/account_assign?search={emp_ref.employee_id}">Create</a></td>
            </tr>
        """

    msg += """
        
    </table><br><br>
    """
    # print(msg)
    return msg


def remove_account_content(emp_ref, emplyee_account_set, user_name, host):
    msg = f"""
        The following accounts of Employee {emp_ref.employee_id}: {emp_ref.name} need to be deleted<br><br>
        If you have any questions, please contact {user_name}<br><br>
        <table>
            <tr>
                <th>Account_Type</th>
                <th>Account</th>
                <th>Person_In_Charge</th>
                <th>Action</th>
            </tr>
            
    """
    for emp_acc in emplyee_account_set:
        msg += f"""
            <tr>
                <td>{emp_acc.account_type_id}</td>
                <td>{emp_acc.account}</td>
                <td>{emp_acc.account_type.person_in_charge}</td>
                <td><a href="http://{host}/account/account_assign?search={emp_ref.employee_id}">Delete</a></td>
            </tr>
        """

    msg += """
        
    </table><br><br>
    """
    # print(msg)
    return msg


def remove_asset_content(emp_ref, asset_list, user_name, host):
    msg = f"""
        The following assets of Employee {emp_ref.employee_id}: {emp_ref.name} need to be deleted<br><br>
        If you have any questions, please contact {user_name}<br><br>
        <table>
            <tr>
                <th>Asset_Type</th>
                <th>Asset_ID</th>
                <th>Person_In_Charge</th>
                <th>Action</th>
            </tr>
            
    """
    for emp_asset in asset_list:
        msg += f"""
            <tr>
                <td>{emp_asset['asset_type']}</td>
                <td>{emp_asset['asset_id']}</td>
                <td>Helpdesk</td>
                <td><a href="http://{host}/asset/asset_assign?search={emp_ref.employee_id}">Delete</a></td>
            </tr>
        """

    msg += """
        
    </table><br><br>
    """
    # print(msg)
    return msg
