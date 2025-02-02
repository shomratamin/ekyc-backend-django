from django.db import models
from .bank import Bank

global DEFAULT_BANK_SETTINGS
DEFAULT_BANK_SETTINGS = {
    'customer_name_eng_req' : ['Customer Name English','true'],
    'customer_name_ben_req' : ['Customer Name Bengali','true'],
    'father_name_req' : ["Father's Name",'true'],
    'mother_name_req' : ["Mother's Name",'true'],
    'dob_req' : ['Date of Birth','true'],
    'address_req' : ['Address','true'],
    'blood_group_req' : ['Blood Group','true'],
    'customer_name_eng_thresh' : ['Customer Name English','80'],
    'customer_name_ben_thresh' : ['Customer Name Bengali','80'],
    'father_name_thresh' : ["Father's Name",'80'],
    'mother_name_thresh' : ["Mother's Name",'80'],
    'dob_thresh' : ['Date of Birth','100'],
    'address_thresh' : ['Address','70'],
    'blood_group_thresh' : ['Blood Group','100'],
    'face_app_thresh' : ['Face App','65'],
    'face_card_thresh' : ['Face Card','65'],
    'auth_token_timeout' : ['Token Timeout','86400'],
    'otp_length' : ['OTP Length', '4'],
    'otp_timeout' : ['OTP Timeout', '180'],
    'mobile_number_length': ['Mobile Number Length','11'],
    'send_registartion_sms_to_agent_bool' : ['Send Registration SMS to Agent', 'true'],
    'onboarding_gender_options' : ['Gender Options', '[]'],
    'onboarding_profession_options' : ['Profession Options', '[]'],
    'onboarding_religion_options' : ['Religion Options', '[]'],
    'onboarding_country_options' : ['Country Options', '[]'],
    'onboarding_source_of_fund_options' : ['Source of fund Options', '[]'],
    'onboarding_account_operation_type_options' : ['Account Operation Type Options', '[]'],
    'onboarding_account_type_options' : ['Profession Options', '[]'],
    'onboarding_additional_services_list' : ['Profession Options', '[]'],
    
}

class BankSetting(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    param = models.CharField(max_length=100)
    value = models.CharField(max_length=2000)
    deletable = models.BooleanField(default=True)
    bank = models.ForeignKey(Bank,on_delete=models.CASCADE,to_field='slug')



def get_default_bank_settings(bank):
    global DEFAULT_BANK_SETTINGS
    all_default_bank_settings = []
    for param in DEFAULT_BANK_SETTINGS:
        value = DEFAULT_BANK_SETTINGS[param]
        bank_setting = BankSetting(name=value[0],param=param,value=value[1],deletable=False,bank=bank)
        all_default_bank_settings.append(bank_setting)
    return all_default_bank_settings
