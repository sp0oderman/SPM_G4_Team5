import os
from dotenv import load_dotenv
from mailersend import emails

API_KEY = os.getenv('EMAIL_API_KEY')
mailer = emails.NewEmail(API_KEY)

# Email notification to Manager of new WFH Request from Employee in team
def newRequestEmailNotif(reporting_manager, employee, wfh_request):

    # define an empty dict to populate with mail values
    mail_body = {}

    mail_from = {
        "name": "WFH System",
        "email": "spmg4t5@trial-0r83ql31w1mgzw1j.mlsender.net"
    }

    recipients = [
        {
            "name": reporting_manager.staff_fname,
            "email": reporting_manager.email,
        }
    ]

    reply_to = {
        "name": "Name",
        "email": "reply@domain.com",
    }

    content =   f"""
                <p>For Reporting Manger: {reporting_manager.staff_fname} {reporting_manager.staff_lname}</p>
                <p>An employee under you has made a new WFH Request.</p>
                <p><b><u>WFH Request Details</u></b><br>
                    <b>Employee ID:</b> {employee.staff_id}<br>
                    <b>Employee Name:</b> {employee.staff_fname} {employee.staff_lname}<br>
                    <b>Request ID:</b> {wfh_request.request_id}<br>
                    <b>Arrangement Type:</b> {wfh_request.arrangement_type}<br>
                    <b>Chosen Date:</b> {wfh_request.chosen_date}<br>
                    <b>Time of Request:</b> {wfh_request.request_datetime}<br>
                    <b>Status:</b> {wfh_request.status}<br>
                    <b>Remarks (if any):</b> ${wfh_request.remarks}<br>
                <p>This is an automated notification system.</p>
                <p>If you have received this notification by accident, please contact the WFH System Team directly</p>
                """


    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject("[WFH System] Notice of new WFH Request", mail_body)
    mailer.set_html_content(content, mail_body)
    mailer.set_plaintext_content("This is the text content", mail_body)
    mailer.set_reply_to(reply_to, mail_body)


    # using print() will also return status code and data
    mailer.send(mail_body)

# Email notification to Employee of WFH Request approval 
def newRequestEmailNotif(reporting_manager, employee, wfh_request):

    # define an empty dict to populate with mail values
    mail_body = {}

    mail_from = {
        "name": "WFH System",
        "email": "spmg4t5@trial-0r83ql31w1mgzw1j.mlsender.net"
    }

    recipients = [
        {
            "name": reporting_manager.staff_fname,
            "email": reporting_manager.email,
        }
    ]

    reply_to = {
        "name": "Name",
        "email": "reply@domain.com",
    }

    content =   f"""
                <p>For Reporting Manger: {reporting_manager.staff_fname} {reporting_manager.staff_lname}</p>
                <p>An employee under you has made a new WFH Request.</p>
                <p><b><u>WFH Request Details</u></b><br>
                    <b>Employee ID:</b> {employee.staff_id}<br>
                    <b>Employee Name:</b> {employee.staff_fname} {employee.staff_lname}<br>
                    <b>Request ID:</b> {wfh_request.request_id}<br>
                    <b>Arrangement Type:</b> {wfh_request.arrangement_type}<br>
                    <b>Chosen Date:</b> {wfh_request.chosen_date}<br>
                    <b>Time of Request:</b> {wfh_request.request_datetime}<br>
                    <b>Status:</b> {wfh_request.status}<br>
                    <b>Remarks (if any):</b> ${wfh_request.remarks}<br>
                <p>This is an automated notification system.</p>
                <p>If you have received this notification by accident, please contact the WFH System Team directly</p>
                """


    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject("[WFH System] Notice of new WFH Request", mail_body)
    mailer.set_html_content(content, mail_body)
    mailer.set_plaintext_content("This is the text content", mail_body)
    mailer.set_reply_to(reply_to, mail_body)


    # using print() will also return status code and data
    mailer.send(mail_body)