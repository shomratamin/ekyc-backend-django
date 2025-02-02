from django.db import models
from django.contrib.auth.models import AbstractUser
from bank.models import Branch, Bank
from customer.models import CustomerProfile
from datetime import datetime, timedelta
import random
from django.utils.timezone import utc

class User(AbstractUser):
    USER_TYPES = (
       ("superadmin", "superadmin"),
       ("admin", "admin"),
       ("bank", "bank"),
       ("agent", "agent"),
       ("checker", "checker"),
       ("maker", "maker"),
       ("customer", "customer")
    )
    USER_TYPES_MAP = dict(USER_TYPES)
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100,default=None, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    is_verified = models.BooleanField(default=True)
    mobile_no = models.CharField(null=True, blank=True, max_length=16)
    user_type = models.CharField(choices=USER_TYPES,max_length=28)
    bank = models.ForeignKey(Bank,on_delete=models.SET_NULL,to_field='slug', null=True, blank=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL, null=True, blank=True)
    customer_profile = models.ForeignKey(CustomerProfile,on_delete=models.SET_NULL, null=True, blank=True)
    cbs_id = models.CharField(max_length=100,default=None, null=True, blank=True)
    cbs_username = models.CharField(max_length=100,default=None, null=True, blank=True)
    cbs_password = models.CharField(max_length=100,default=None, null=True, blank=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','user_type']


class OtpAuth(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   mobile_or_email = models.CharField(max_length=100)
   otp = models.CharField(max_length=12)
   expires_on = models.DateTimeField()

def generate_otp(user, expire_seconds=300):
   status = False
   if OtpAuth.objects.filter(user=user).exists():
      OtpAuth.objects.filter(user=user).delete()

   expires_on = datetime.utcnow().replace(tzinfo=utc) + timedelta(seconds=expire_seconds)
   otp = random.randrange(100001, 999999)
   otp_auth = OtpAuth(user=user,mobile_or_email=user.mobile_no,otp=otp, expires_on=expires_on)
   otp_auth.save()
   status = True
   return status, otp

def generate_otp_agent(user, mobile_or_email, expire_seconds=300):
   status = False
   if OtpAuth.objects.filter(user=user).exists():
      OtpAuth.objects.filter(user=user).delete()

   expires_on = datetime.utcnow().replace(tzinfo=utc) + timedelta(seconds=expire_seconds)
   otp = random.randrange(100001, 999999)
   otp_auth = OtpAuth(user=user,mobile_or_email=mobile_or_email,otp=otp, expires_on=expires_on)
   otp_auth.save()
   status = True
   return status, otp


def otp_valid(otp_expires_on, time_limit=300):
   now = datetime.utcnow().replace(tzinfo=utc)
   time_difference = otp_expires_on - now
   print('now is', now)
   print('otp expires on', otp_expires_on)
   time_difference = time_difference.total_seconds()
   print('otp time difference', time_difference)
   if time_difference > time_limit:
      return False

   return True

def verify_otp(mobile_or_email, otp):
   status = False
   user = None
   otp_auth = OtpAuth.objects.filter(mobile_or_email=mobile_or_email, otp=otp)

   if otp_auth.exists():
      otp = otp_auth.first()
      status = otp_valid(otp.expires_on)
      user = otp.user
      otp.delete()

   return status, user

def verify_otp_joint(user, otp):
   status = False
   mobile_no = None
   otp_auth = OtpAuth.objects.filter(user=user, otp=otp)

   if otp_auth.exists():
      otp = otp_auth.first()
      status = otp_valid(otp.expires_on)
      mobile_no = otp.mobile_or_email
      otp.delete()

   return status, mobile_no