import os
from dotenv import load_dotenv

# Libraries for email sending
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load env variables to be used
load_dotenv()

EMAIL_ACCOUNT = os.getenv('EMAIL_ACCOUNT')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Email notification to Manager of new WFH Request from Employee in team
def newRequestEmailNotif(reporting_manager, employee, wfh_request):

    recipients = reporting_manager.email

    email_body = f"""
                <html><body>
                <p>For Manager: {reporting_manager.staff_fname} {reporting_manager.staff_lname}.</p>
                <p>An employee in your team has made a new WFH Request.</p>
                <p><b><u>WFH Request Details</u></b><br>
                    <b>Employee Name:</b> {employee.staff_fname} {employee.staff_lname}<br>
                    <b>Employee ID:</b> {employee.staff_id}<br>
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

    message['Subject'] = '[WFH System] New WFH application for your review'
    message['From'] = "spmg4t5@gmail.com"
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


# Email notification to Employee of WFH Request approval or rejection
def approvalOrRejectionEmailNotif(reporting_manager, employee, wfh_request):

    recipients = employee.email

    email_body = f"""
                <html><body>
                <p>For Staff: {employee.staff_fname} {employee.staff_lname}</p>
                <p>Your WFH Request has been {wfh_request.status.lower()} by Reporting Manager: {reporting_manager.staff_fname} {reporting_manager.staff_lname}.</p>
                <p><b><u>WFH Request Details</u></b><br>
                    <b>Employee ID:</b> {employee.staff_id}<br>
                    <b>Employee Name:</b> {employee.staff_fname} {employee.staff_lname}<br>
                    <b>Request ID:</b> {wfh_request.request_id}<br>
                    <b>Arrangement Type:</b> {wfh_request.arrangement_type}<br>
                    <b>Chosen Date:</b> {wfh_request.chosen_date}<br>
                    <b>Time of Request:</b> {wfh_request.request_datetime}<br>
                    <b>Status:</b> {wfh_request.status}<br>
                    <b>Remarks (if any):</b> {wfh_request.remarks}<br>
                <p>This is an automated notification system.</p>
                <p>If you have received this notification by accident, please contact the WFH System Team directly!</p>
                </body></html>
                """

    message = MIMEMultipart('alternative', None, [MIMEText(email_body, 'html')])

    message['Subject'] = f"[WFH System] Notice of {wfh_request.status} WFH Request"
    message['From'] = "spmg4t5@gmail.com"
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
def withdrawRequestEmailNotif(reporting_manager, employee, wfh_request):

    recipients = employee.email

    email_body = f"""
                <html><body>
                <p>For Staff: {employee.staff_fname} {employee.staff_lname}</p>
                <p>Your previously approved WFH Request has been withdrawn by Reporting Manager: {reporting_manager.staff_fname} {reporting_manager.staff_lname}.</p>
                <p><b><u>WFH Request Details</u></b><br>
                    <b>Employee ID:</b> {employee.staff_id}<br>
                    <b>Employee Name:</b> {employee.staff_fname} {employee.staff_lname}<br>
                    <b>Request ID:</b> {wfh_request.request_id}<br>
                    <b>Arrangement Type:</b> {wfh_request.arrangement_type}<br>
                    <b>Chosen Date:</b> {wfh_request.chosen_date}<br>
                    <b>Time of Request:</b> {wfh_request.request_datetime}<br>
                    <b>Status:</b> {wfh_request.status}<br>
                    <b>Remarks (if any):</b> {wfh_request.remarks}<br>
                <p>This is an automated notification system.</p>
                <p>If you have received this notification by accident, please contact the WFH System Team directly!</p>
                </body></html>
                """

    message = MIMEMultipart('alternative', None, [MIMEText(email_body, 'html')])

    message['Subject'] = "[WFH System] Notice of previously Approved WFH Request being withdrawn"
    message['From'] = "spmg4t5@gmail.com"
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