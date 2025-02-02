from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template import Template, Context
from email.mime.image import MIMEImage

global send_otp_template, tracking_number_template, password_email_template, logo

logo = "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"

send_otp_template = '''<body style="margin:0; padding: 0;box-sizing: border-box;">
    <div style="width: 60%; border: 1px solid #000; margin: 100px auto; padding: 30px;">
        <div>
            <span></span>

            <span style="float: right;">
                <img src="cid:logo" />
                </span>
        </div>
        <p>Dear Customer, </p>

        To authenticate your IFIC Digital Account Opening Registration, please use the One Time Password (OTP):
        <h2>{{ email_otp }}</h2>
        This OTP will expire in 5 minutes. Please do not share this OTP with anyone. IFIC Bank takes your account security seriously. IFIC Bank customer service will never ask you to disclose the OTP.

        <p>Thank You</p>

        <p>IFIC Bank Limited</p>
    </div>
</body>'''

tracking_number_template = '''<body style="margin:0; padding: 0;box-sizing: border-box;">
    <div style="width: 60%; border: 1px solid #000; margin: 100px auto; padding: 30px;">
        <div>
            <span></span>

            <span style="float: right;">
                <img src="cid:logo" />
            </span>
        </div>

        <p>Dear Customer, </p>
        <h2>Congratulations !!</h2>
        <p>You have successfully completed IFIC Digital Account Opening Registration process.<br>
        Your tracking number is : {{tracking_number}}<br>
        Please visit your nearest IFIC Branch/Uposhakha with your registration number to complete the Account Opening process within 3 Months.</p>
        <p>For any query please call 16255 (Local) or +8809666716255 (Abroad)</p>

        <p>Thank You</p>

        <p>IFIC Bank Limited</p>
    </div>
</body>'''

password_email_template = '''<body style="margin:0; padding: 0;box-sizing: border-box;">
    <div style="width: 60%; border: 1px solid #000; margin: 100px auto; padding: 30px;">
        <div>
            <span></span>

            <span style="float: right;">
                <img src="cid:logo" />
            </span>
        </div>

        <p>Your EKYC login password is : <h3>{{password}}</h3>
        Please don't share it with anyone.</p>

        <p>Thank You</p>

        <p>IFIC Bank Limited</p>
    </div>
</body>'''

password_reset_email_template = '''<body style="margin:0; padding: 0;box-sizing: border-box;">
    <div style="width: 60%; border: 1px solid #000; margin: 100px auto; padding: 30px;">
        <div>
            <span></span>

            <span style="float: right;">
                <img src="cid:logo" />
            </span>
        </div>

        <p>Please visit this link to reset your password : <a target="_blank" href="{{reset_token_link}}">{{reset_token_link}}</a>, please don't share it with anyone.</p>

        <p>Thank You</p>

        <p>IFIC Bank Limited</p>
    </div>
</body>'''

def send_otp_email(email, otp):
    global send_otp_template, logo

    data = Context({'email_otp': otp})
    email_body = Template(send_otp_template)
    email_body = email_body.render(data)
    send_mail('IFIC Digital Account Opening Registration', '', settings.EMAIL_HOST_USER, [email], html_message=email_body)
    msg = EmailMultiAlternatives('IFIC Digital Account Opening Registration', '', settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(email_body, "text/html")
    img = MIMEImage(logo, 'png')
    img.add_header('Content-Id', 'logo')
    img.add_header("Content-Disposition", "inline", filename="logo.png")
    msg.attach(img)
    msg.send(fail_silently=False)

def send_tracking_number_email(email, tracking_number):
    global tracking_number_template
    data = Context({'tracking_number': tracking_number})
    email_body = Template(tracking_number_template)
    email_body = email_body.render(data)
    send_mail('IFIC Bank EKYC Account Creation Success', '', settings.EMAIL_HOST_USER, [email], html_message=email_body)

def send_password_email(email, password):
    global password_email_template
    data = Context({'password': password})
    email_body = Template(password_email_template)
    email_body = email_body.render(data)
    send_mail('IFIC EKYC Password', '', settings.EMAIL_HOST_USER, [email], html_message=email_body)

def send_password_reset_email(email, reset_token_link):
    global password_email_template
    data = Context({'reset_token_link': reset_token_link})
    email_body = Template(password_reset_email_template)
    email_body = email_body.render(data)
    send_mail('IFIC EKYC Password Reset Link', '', settings.EMAIL_HOST_USER, [email], html_message=email_body)

