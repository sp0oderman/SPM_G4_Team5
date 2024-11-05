import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Libraries for email sending
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load env variables to be used
load_dotenv()

EMAIL_ACCOUNT = os.getenv('EMAIL_ACCOUNT')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

########################################################################################################################################################################################################################################

# Email notification to Manager of new WFH Request from Employee in team
def newWFHRequestEmailNotif(reporting_manager, employee, wfh_request):

    recipients = reporting_manager.email

    email_body = f"""
                <html><body>
                <p>Dear {reporting_manager.staff_fname} {reporting_manager.staff_lname},</p>
                <p>An employee in your team has made a new WFH Request.</p>
                <p><b><u>WFH Request Details</u></b><br>
                    <b>Employee Name:</b> {employee.staff_fname} {employee.staff_lname}<br>
                    <b>Employee ID:</b> {employee.staff_id}<br>
                    <b>Employee ID:</b> {employee.staff_id}<br>
                    <b>Request ID:</b> {wfh_request.request_id}<br>
                    <b>Arrangement Type:</b> {wfh_request.arrangement_type}<br>
                    <b>Chosen Date:</b> {wfh_request.chosen_date}<br>
                    <b>Time of Request:</b> {wfh_request.request_datetime}<br>
                    <b>Status:</b> {wfh_request.status}<br>
                    <b>Remarks:</b> {wfh_request.remarks}<br>
                <p>This is an automated notification.</p>
                <p>If you have received this notification by accident, please contact the WFH System developers via spmg4t5@gmail.com.</p>
                </body></html>
                """

    message = MIMEMultipart('alternative', None, [MIMEText(email_body, 'html')])

    message['Subject'] = '[WFH System] New WFH application for your review'
    message['From'] = EMAIL_ACCOUNT
    message['To'] = reporting_manager.email

    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ACCOUNT, recipients, message.as_string())
        server.quit()
        print(f"Email sent: {email_body}")
    except Exception as e:
        print(f"Error in sending email: {e}")


# Email notification to Employee of WFH Request approval or rejection
def approvalOrRejectionWFHRequestEmailNotif(reporting_manager, employee, wfh_request):

    recipients = employee.email

    email_body = f"""
                <html><body>
                <p>Dear {employee.staff_fname} {employee.staff_lname},</p>
                <p>Your WFH Request has been <b><u>{wfh_request.status.lower()}</u></b> by your reporting manager, {reporting_manager.staff_fname} {reporting_manager.staff_lname}.</p>
                <p><b><u>WFH Request Details</u></b><br>
                    <b>Employee ID:</b> {employee.staff_id}<br>
                    <b>Employee Name:</b> {employee.staff_fname} {employee.staff_lname}<br>
                    <b>Request ID:</b> {wfh_request.request_id}<br>
                    <b>Arrangement Type:</b> {wfh_request.arrangement_type}<br>
                    <b>Chosen Date:</b> {wfh_request.chosen_date}<br>
                    <b>Time of Request:</b> {wfh_request.request_datetime}<br>
                    <b>Status:</b> {wfh_request.status}<br>
                    <b>Remarks (if any):</b> {wfh_request.remarks}<br>
                <p>This is an automated notification.</p>
                <p>If you have received this notification by accident, please contact the WFH System developers via spmg4t5@gmail.com.</p>
                </body></html>
                """

    message = MIMEMultipart('alternative', None, [MIMEText(email_body, 'html')])

    message['Subject'] = f"[WFH System] Notice of {wfh_request.status} WFH Request"
    message['From'] = EMAIL_ACCOUNT
    message['To'] = employee.email

    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ACCOUNT, recipients, message.as_string())
        server.quit()
        print(f"Email sent successfully!")
    except Exception as e:
        print(f"Error in sending email: {e}")


# Email notification to Employee of Approved WFH Request being withdrawn by Reporting Manager
def withdrawWFHRequestEmailNotif(reporting_manager, employee, wfh_request):

    recipients = employee.email

    email_body = f"""
                <html><body>
                <p>Dear {employee.staff_fname} {employee.staff_lname},</p>
                <p>Your previously approved WFH Request has been withdrawn by your reporting manager, {reporting_manager.staff_fname} {reporting_manager.staff_lname}.</p>
                <p><b><u>WFH Request Details</u></b><br>
                    <b>Employee ID:</b> {employee.staff_id}<br>
                    <b>Employee Name:</b> {employee.staff_fname} {employee.staff_lname}<br>
                    <b>Request ID:</b> {wfh_request.request_id}<br>
                    <b>Arrangement Type:</b> {wfh_request.arrangement_type}<br>
                    <b>Chosen Date:</b> {wfh_request.chosen_date}<br>
                    <b>Time of Request:</b> {wfh_request.request_datetime}<br>
                    <b>Status:</b> {wfh_request.status}<br>
                    <b>Remarks (if any):</b> {wfh_request.remarks}<br>
                <p>This is an automated notification.</p>
                <p>If you have received this notification by accident, please contact the WFH System developers via spmg4t5@gmail.com.</p>
                </body></html>
                """

    message = MIMEMultipart('alternative', None, [MIMEText(email_body, 'html')])

    message['Subject'] = "[WFH System] Notice of withdrawn WFH Request"
    message['From'] = EMAIL_ACCOUNT
    message['To'] = employee.email

    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ACCOUNT, recipients, message.as_string())
        server.quit()
        print(f"Email sent successfully!")
    except Exception as e:
        print(f"Error in sending email: {e}")

########################################################################################################################################################################################################################################

# Email notification to Manager of new Withdrawal Request from Employee in team
def newWithdrawalRequestEmailNotif(reporting_manager, employee, withdrawal_request):

    recipients = reporting_manager.email

    email_body = f"""
                <html><body>
                <p>Dear {reporting_manager.staff_fname} {reporting_manager.staff_lname},</p>
                <p>An employee in your team has made a new Withdrawal Request.</p>
                <p><b><u>Withdrawal Request Details</u></b><br>
                    <b>Employee Name:</b> {employee.staff_fname} {employee.staff_lname}<br>
                    <b>Employee ID:</b> {employee.staff_id}<br>
                    <b>Withdrawal Request ID:</b> {withdrawal_request.request_id}<br>
                    <b>Affected WFH Request ID:</b> {withdrawal_request.wfh_request_id}<br>
                    <b>Time of Request:</b> {withdrawal_request.request_datetime}<br>
                    <b>Status:</b> {withdrawal_request.status}<br>
                    <b>Remarks (if any):</b> {withdrawal_request.remarks}<br>
                <p>This is an automated notification.</p>
                <p>If you have received this notification by accident, please contact the WFH System developers via spmg4t5@gmail.com.</p>
                </body></html>
                """

    message = MIMEMultipart('alternative', None, [MIMEText(email_body, 'html')])

    message['Subject'] = '[WFH System] New WFH withdrawal request for your review'
    message['From'] = EMAIL_ACCOUNT
    message['To'] = reporting_manager.email

    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ACCOUNT, recipients, message.as_string())
        server.quit()
        print(f"Email sent successfully!")
    except Exception as e:
        print(f"Error in sending email: {e}")


# Email notification to Employee of withdrawal_request approval or rejection
def approvalOrRejectionWithdrawalRequestEmailNotif(reporting_manager, employee, withdrawal_request):

    recipients = employee.email

    email_body = f"""
                <html><body>
                <p>Dear {employee.staff_fname} {employee.staff_lname},</p>
                <p>Your Withdrawal Request has been <b><u>{withdrawal_request.status.lower()}</u></b> by your reporting manager, {reporting_manager.staff_fname} {reporting_manager.staff_lname}.</p>
                <p><b><u>Withdrawal Request Details</u></b><br>
                    <b>Employee ID:</b> {employee.staff_id}<br>
                    <b>Employee Name:</b> {employee.staff_fname} {employee.staff_lname}<br>
                    <b>Withdrawal Request ID:</b> {withdrawal_request.request_id}<br>
                    <b>Affected WFH Request ID:</b> {withdrawal_request.wfh_request_id}<br>
                    <b>Time of Request:</b> {withdrawal_request.request_datetime}<br>
                    <b>Status:</b> {withdrawal_request.status}<br>
                    <b>Remarks (if any):</b> {withdrawal_request.remarks}<br>
                <p>This is an automated notification.</p>
                <p>If you have received this notification by accident, please contact the WFH System developers via spmg4t5@gmail.com.</p>
                </body></html>
                """

    message = MIMEMultipart('alternative', None, [MIMEText(email_body, 'html')])

    message['Subject'] = f"[WFH System] Notice of {withdrawal_request.status} Withdrawal Request"
    message['From'] = EMAIL_ACCOUNT
    message['To'] = employee.email

    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ACCOUNT, recipients, message.as_string())
        server.quit()
        print(f"Email sent successfully!")
    except Exception as e:
        print(f"Error in sending email: {e}")