from datetime import date
from django.db import models
from bank.models import Bank
from bank.models import Branch
from django.utils import timezone
import uuid, string, random

def random_string(stringLength=32):
    letters = ''.join([string.ascii_lowercase, string.ascii_uppercase, string.digits])
    return ''.join(random.choice(letters) for i in range(stringLength))

class CustomerVerificationScores(models.Model):
    customer_name_eng_score = models.IntegerField(default=-1)
    customer_name_eng_status = models.CharField(max_length=20,default='pending')
    customer_name_ben_score = models.IntegerField(default=-1)
    customer_name_ben_status = models.CharField(max_length=20,default='pending')
    father_name_score = models.IntegerField(default=-1)
    father_name_status = models.CharField(max_length=20,default='pending')
    mother_name_score = models.IntegerField(default=-1)
    mother_name_status = models.CharField(max_length=20,default='pending')
    spouse_name_score = models.IntegerField(default=-1)
    spouse_name_status = models.CharField(max_length=20,default='pending')
    present_addrress_score = models.IntegerField(default=-1)
    present_addrress_status = models.CharField(max_length=20,default='pending')
    customer_photo_card_score = models.IntegerField(default=-1)
    customer_photo_card_status = models.CharField(max_length=20,default='pending')
    customer_photo_app_score = models.IntegerField(default=-1)
    customer_photo_app_status = models.CharField(max_length=20,default='pending')
    textual_info_match_status = models.CharField(max_length=20,default='pending')

class CustomerScreeningInfo(models.Model):
    is_pep = models.BooleanField(default=False)
    pep_check_status = models.CharField(max_length=20,default='pending')

class AdditionalServices(models.Model):
    cheque_book = models.BooleanField(default=False)
    debit_card = models.BooleanField(default=False)
    sms_alert = models.BooleanField(default=False)
    digital_banking = models.BooleanField(default=False)
    e_statement_facility = models.BooleanField(default=False)


class CustomerProfile(models.Model):
    tracking_number = models.CharField(max_length=20,default=None,null=True, blank=True)
    customer_uuid = models.CharField(max_length=40,default=None, blank=True, null=True, editable=False)
    customer_short_name = models.CharField(max_length=50,default=None, null=True, blank=True)
    account_status = models.CharField(max_length=20,default='pending')
    nid_no = models.CharField(max_length=50,default=None, null=True, blank=True)
    id_type = models.CharField(max_length=100,default=None, null=True, blank=True)
    dob = models.CharField(max_length=50,default=None, null=True, blank=True)
    customer_name_eng = models.CharField(max_length=100,default=None,null=True, blank=True)
    nominee = models.CharField(max_length=100,default=None,null=True, blank=True)
    nominee_relation_profile = models.CharField(max_length=100,default=None,null=True, blank=True)
    customer_name_ben = models.CharField(max_length=100,default=None,null=True, blank=True)
    father_name_eng = models.CharField(max_length=100,default=None,null=True, blank=True)
    father_name_ben = models.CharField(max_length=100,default=None,null=True, blank=True)
    mother_name_eng = models.CharField(max_length=100,default=None,null=True, blank=True)
    mother_name_ben = models.CharField(max_length=100,default=None,null=True, blank=True)
    spouse_name_eng = models.CharField(max_length=100,default=None,null=True, blank=True)
    spouse_name_ben = models.CharField(max_length=100,default=None,null=True, blank=True)
    gender = models.CharField(max_length=30,default=None,null=True, blank=True)

    pres_address_eng = models.CharField(max_length=1000,default=None,null=True, blank=True)
    pres_address_eng_line1 = models.CharField(max_length=100,default=None,null=True, blank=True)
    pres_address_eng_line2 = models.CharField(max_length=100,default=None,null=True, blank=True)
    pres_address_eng_line3 = models.CharField(max_length=100,default=None,null=True, blank=True)
    pres_address_eng_line4 = models.CharField(max_length=100,default=None,null=True, blank=True)
    pres_address_ben = models.CharField(max_length=1000,default=None,null=True, blank=True)
    perm_address_eng = models.CharField(max_length=1000,default=None,null=True, blank=True)
    perm_address_eng_line1 = models.CharField(max_length=100,default=None,null=True, blank=True)
    perm_address_eng_line2 = models.CharField(max_length=100,default=None,null=True, blank=True)
    perm_address_eng_line3 = models.CharField(max_length=100,default=None,null=True, blank=True)
    perm_address_eng_line4 = models.CharField(max_length=100,default=None,null=True, blank=True)
    perm_address_ben = models.CharField(max_length=1000,default=None,null=True, blank=True)
    prof_address_eng = models.CharField(max_length=1000,default=None,null=True, blank=True)
    prof_address_eng_line1 = models.CharField(max_length=100,default=None,null=True, blank=True)
    prof_address_eng_line2 = models.CharField(max_length=100,default=None,null=True, blank=True)
    prof_address_eng_line3 = models.CharField(max_length=100,default=None,null=True, blank=True)
    prof_address_eng_line4 = models.CharField(max_length=100,default=None,null=True, blank=True)
    prof_address_ben = models.CharField(max_length=1000,default=None,null=True, blank=True)

    mailing_address = models.CharField(max_length=50,default=None, null=True, blank=True)
    tin_number = models.CharField(max_length=28,default=None, null=True, blank=True)
    etin_number = models.CharField(max_length=28,default=None, null=True, blank=True)
    nid_front_image = models.CharField(max_length=100,default=None, null=True, blank=True)
    nid_back_image = models.CharField(max_length=100,default=None, null=True, blank=True)
    customer_photo_from_card_image = models.CharField(max_length=100,default=None, null=True, blank=True)
    customer_photo_from_app_image = models.CharField(max_length=100,default=None, null=True, blank=True)
    customer_photo_other_from_app_image = models.CharField(max_length=100,default=None, null=True, blank=True)
    profession = models.CharField(max_length=100,default=None, null=True, blank=True)
    other_profession = models.CharField(max_length=100,default=None, null=True, blank=True)
    mobile_number = models.CharField(max_length=20,default=None, null=True, blank=True)
    mobile_number_verified = models.BooleanField(default=False)
    email = models.CharField(max_length=100,default=None, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    verification_status = models.CharField(max_length=50,default='pending')
    verification_scores = models.ForeignKey(CustomerVerificationScores,on_delete=models.SET_NULL,null=True, blank=True)
    screening_info = models.ForeignKey(CustomerScreeningInfo,on_delete=models.SET_NULL,null=True, blank=True)
    screening_status = models.CharField(max_length=50,default='pending')
    on_boarded_by = models.IntegerField(default=None, null=True, blank=True)
    religion = models.CharField(max_length=50,default=None, null=True, blank=True)
    place_of_birth = models.CharField(max_length=100,default=None, null=True, blank=True)
    country_of_birth = models.CharField(max_length=100,default=None, null=True, blank=True)
    source_of_fund = models.CharField(max_length=100,default=None, null=True, blank=True)
    other_source_of_fund = models.CharField(max_length=100,default=None, null=True, blank=True)
    nature_of_business = models.CharField(max_length=100,default=None, null=True, blank=True)
    native_resident = models.BooleanField(default=True)
    residential_status = models.CharField(max_length=50,default=None, null=True, blank=True)

    transaction_limit_monthly = models.CharField(max_length=50,default=None,null=True, blank=True)
    editing_account_type = models.CharField(max_length=100,default=None, null=True, blank=True)
    editing_account_uuid = models.CharField(max_length=100,default=None, null=True, blank=True)

    nationality = models.CharField(max_length=100,default=None, null=True, blank=True)
    monthly_income = models.CharField(max_length=100,default=None, null=True, blank=True)
    
    us_residency = models.BooleanField(default=False)
    us_citizenship = models.BooleanField(default=False)
    us_pr_card = models.BooleanField(default=False)
    us_have_residence_address = models.BooleanField(default=False)
    us_have_correspondence_address = models.BooleanField(default=False)
    us_address = models.CharField(max_length=100,default=None, null=True, blank=True)
    us_social_security_number = models.CharField(max_length=50,default=None, null=True, blank=True)
    us_contact_number = models.CharField(max_length=100,default=None, null=True, blank=True)
    
    nrf_reason_for_acc_opening = models.CharField(max_length=500,default=None, null=True, blank=True)
    nrf_type_of_visa_resident = models.BooleanField(default=False)
    nrf_type_of_visa_work = models.BooleanField(default=False)
    nrf_visa_validity_upto = models.CharField(max_length=50,default=None,null=True, blank=True)
    nrf_work_permit_letter_obtained = models.BooleanField(default=False)

    bank = models.ForeignKey(Bank,on_delete=models.SET_NULL,to_field='slug', null=True, blank=True)
    preferred_branch = models.CharField(max_length=50,default=None,null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=False, editable=False)
    submitted_on = models.DateTimeField(auto_now_add=False)
    updated_on = models.DateTimeField(auto_now=False)

    def as_dict(self):
        return {'id': '{}'.format(self.id),'mobile_number': self.mobile_number,'applicant_name_eng': self.customer_name_eng,'nid_no': self.nid_no,'submitted_on': self.submitted_on,'verification_status': self.verification_status}

    def as_list(self):
        return [self.nid_no, self.customer_name_eng, self.mobile_number ]

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.customer_uuid = random_string()
            self.created_on = timezone.now()
            self.submitted_on = timezone.now()
        self.updated_on = timezone.now()
        return super(CustomerProfile, self).save(*args, **kwargs)


class CustomerAccount(models.Model):
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,null=True, blank=True, related_name='first_applicant')
    tracking_number = models.CharField(max_length=20,default=None,null=True, blank=True)
    uuid = models.CharField(max_length=40,default=None, blank=True, null=True, editable=False)
    branch_code = models.CharField(max_length=50,default=None,null=True, blank=True)
    preferred_branch_code = models.CharField(max_length=50,default=None,null=True, blank=True)
    onboarding_type = models.CharField(max_length=50,default=None,null=True, blank=True)
    account_type = models.CharField(max_length=100,default=None, null=True, blank=True)
    purpose_of_account_opening = models.CharField(max_length=500,default=None, null=True, blank=True)
    account_type_bankside = models.CharField(max_length=100,default=None, null=True, blank=True)
    account_operation_type = models.CharField(max_length=50,default='individual',null=True, blank=True)
    account_profile_type = models.CharField(max_length=50,default='simplified',null=True, blank=True)
    account_name = models.CharField(max_length=50,default=None,null=True, blank=True)
    account_number = models.CharField(max_length=50,default=None,null=True, blank=True)
    unique_account_number = models.CharField(max_length=50,default=None,null=True, blank=True)
    transaction_amount_monthly = models.CharField(max_length=50,default=None,null=True, blank=True)
    account_remarks = models.TextField(default=None,null=True, blank=True)
    initial_deposit = models.IntegerField(default=0)
    initial_deposit_text = models.CharField(max_length=100,default=None, null=True, blank=True)
    preferred_currency = models.CharField(max_length=28,default=None, null=True, blank=True)
    joint_mode_of_operation = models.CharField(max_length=50,default=None,null=True, blank=True)
    joint_signatory = models.CharField(max_length=100,default=None,null=True, blank=True)
    joint_signatory_other = models.CharField(max_length=100,default=None,null=True, blank=True)
    joint_number_of_applicants = models.SmallIntegerField(default=3)
    joint_account_title_eng = models.CharField(max_length=100,default=None,null=True, blank=True)
    joint_account_title_ben = models.CharField(max_length=100,default=None,null=True, blank=True)
    joint_second_applicant = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,null=True, blank=True, related_name='joint_second_appicant')
    joint_third_applicant = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,null=True, blank=True, related_name='joint_third_appicant')
    joint_fourth_applicant = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,null=True, blank=True, related_name='joint_fourth_appicant')
    joint_fifth_applicant = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,null=True, blank=True, related_name='joint_fifth_appicant')
    additional_services = models.OneToOneField(AdditionalServices,on_delete=models.SET_NULL, null=True, blank=True)
    approval_status = models.CharField(max_length=50,default='pending')
    approval_status_name = models.CharField(max_length=50,default='pending')
    approval_remarks = models.CharField(max_length=50,default='pending')
    created_on = models.DateTimeField(auto_now_add=False, editable=False)
    submitted_on = models.DateTimeField(auto_now_add=False)
    updated_on = models.DateTimeField(auto_now=False)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.uuid = random_string()
            self.created_on = timezone.now()
            self.submitted_on = timezone.now()
        self.updated_on = timezone.now()
        return super(CustomerAccount, self).save(*args, **kwargs)

    def as_list(self):
        return [self.branch_code, self.account_type]

class CustomerNominee(models.Model):
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,null=True, blank=True, related_name='nominees')
    bank_account = models.ForeignKey(CustomerAccount,on_delete=models.CASCADE,null=True, blank=True, related_name='account_nominees')
    nominee_index = models.SmallIntegerField(default=0)
    nominee_name_eng = models.CharField(max_length=100,default=None,null=True, blank=True)
    nominee_name_ben = models.CharField(max_length=100,default=None,null=True, blank=True)
    nominee_dob = models.CharField(max_length=50,default=None, null=True, blank=True)
    nominee_relation = models.CharField(max_length=100,default=None,null=True, blank=True)
    nominee_pres_address_eng = models.CharField(max_length=1000,default=None,null=True, blank=True)
    nominee_perm_address_eng = models.CharField(max_length=1000,default=None,null=True, blank=True)
    nominee_pres_address_ben = models.CharField(max_length=1000,default=None,null=True, blank=True)
    nominee_perm_address_ben = models.CharField(max_length=1000,default=None,null=True, blank=True)
    nominee_share_percentage = models.CharField(max_length=8,default='0')
    nominee_id_type = models.CharField(max_length=50,default=None,null=True, blank=True)
    nominee_id_number = models.CharField(max_length=50,default=None,null=True, blank=True)
    nominee_id_front_image = models.CharField(max_length=100,default=None, null=True, blank=True)
    nominee_id_back_image = models.CharField(max_length=100,default=None, null=True, blank=True)
    nominee_photo_image = models.CharField(max_length=100,default=None, null=True, blank=True)
    nominee_other_id_image = models.CharField(max_length=100,default=None, null=True, blank=True)
    nominee_tin_number = models.CharField(max_length=28,default=None, null=True, blank=True)
    nominee_account_number = models.CharField(max_length=28,default=None, null=True, blank=True)
    nominee_minor = models.BooleanField(default=False)
    nominee_minor_legal_guardian_name = models.CharField(max_length=100,default=None, null=True, blank=True)
    nominee_minor_legal_guardian_dob = models.CharField(max_length=28,default=None, null=True, blank=True)
    nominee_minor_legal_guardian_pres_address_eng = models.CharField(max_length=1000,default=None, null=True, blank=True)
    nominee_minor_legal_guardian_pres_address_ben = models.CharField(max_length=1000,default=None, null=True, blank=True)
    nominee_minor_legal_guardian_perm_address_eng = models.CharField(max_length=1000,default=None, null=True, blank=True)
    nominee_minor_legal_guardian_perm_address_ben = models.CharField(max_length=1000,default=None, null=True, blank=True)
    nominee_minor_legal_guardian_relation = models.CharField(max_length=100,default=None, null=True, blank=True)
    nominee_minor_legal_guardian_contact_no = models.CharField(max_length=28,default=None, null=True, blank=True)
    nominee_minor_legal_guardian_id_type = models.CharField(max_length=50,default=None, null=True, blank=True)
    nominee_minor_legal_guardian_photo_image = models.CharField(max_length=100,default=None, null=True, blank=True)
    nominee_minor_legal_guardian_id_front_image = models.CharField(max_length=100,default=None, null=True, blank=True)
    nominee_minor_legal_guardian_id_back_image = models.CharField(max_length=100,default=None, null=True, blank=True)
    nominee_minor_legal_guardian_id_number = models.CharField(max_length=50,default=None, null=True, blank=True)

    class Meta:
        ordering = ['nominee_index']


class TransactionProfile(models.Model):
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,null=True, blank=True, related_name='transaction_profile')
    transaction_channel_index = models.PositiveIntegerField(default=0)
    transaction_channel = models.CharField(max_length=100,default=None,null=True, blank=True)
    transaction_deposit_number = models.PositiveIntegerField(default=0)
    transaction_deposit_amount = models.PositiveIntegerField(default=0)
    transaction_deposit_amount_per_max = models.PositiveIntegerField(default=0)
    transaction_withdraw_number = models.PositiveIntegerField(default=0)
    transaction_withdraw_amount = models.PositiveIntegerField(default=0)
    transaction_withdraw_amount_per_max = models.PositiveIntegerField(default=0)

class RiskGrading(models.Model):
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,null=True, blank=True, related_name='risk_grading')
    riskgrading_type_of_onboarding = models.CharField(max_length=100,default=None,null=True, blank=True)
    riskgrading_geographic_risk = models.CharField(max_length=100,default=None,null=True, blank=True)
    riskgrading_is_pep = models.BooleanField(default=False)
    riskgrading_is_ip = models.BooleanField(default=False)
    riskgrading_is_pep_family = models.BooleanField(default=False)
    riskgrading_product_and_channel_risk = models.CharField(max_length=100,default=None,null=True, blank=True)
    riskgrading_business_and_activity_risk = models.CharField(max_length=100,default=None,null=True, blank=True)
    riskgrading_profession_and_activity_risk = models.CharField(max_length=100,default=None,null=True, blank=True)
    riskgrading_businsess_or_profession = models.CharField(max_length=100,default='profession',null=True, blank=True)
    riskgrading_transaction_risk = models.CharField(max_length=100,default=None,null=True, blank=True)
    riskgrading_credible_source_of_fund = models.BooleanField(default=False)
    riskgrading_client_citizenship_ust = models.BooleanField(default=False)
    riskgrading_donates_to_pep = models.BooleanField(default=False)

class RiskGradingScore(models.Model):
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,null=True, blank=True, related_name='risk_grading_score')
    riskgradingscore_type_of_onboarding = models.IntegerField(default=0)
    riskgradingscore_geographic_risk = models.IntegerField(default=0)
    riskgradingscore_is_pep = models.IntegerField(default=0)
    riskgradingscore_is_ip = models.IntegerField(default=0)
    riskgradingscore_is_pep_family = models.IntegerField(default=0)
    riskgradingscore_product_and_channel_risk = models.IntegerField(default=0)
    riskgradingscore_business_and_activity_risk = models.IntegerField(default=0)
    riskgradingscore_profession_and_activity_risk = models.IntegerField(default=0)
    riskgradingscore_transaction_risk = models.IntegerField(default=0)
    riskgradingscore_credible_source_of_fund = models.IntegerField(default=0)
    riskgradingscore_client_citizenship_ust = models.IntegerField(default=0)
    riskgradingscore_donates_to_pep = models.IntegerField(default=0)
    riskgradingscore_score = models.IntegerField(default=0)
    riskgradingscore_assessment_type = models.CharField(default=None, null=True, blank=True, max_length=100)

class RiskAssesment(models.Model):
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,null=True, blank=True, related_name='risk_assessment')
    riskassessment_unscrs_check_done = models.BooleanField(default=False)
    riskassessment_is_pep = models.BooleanField(default=False)
    riskassessment_pep_details = models.CharField(max_length=100,default=None,null=True, blank=True)
    riskassessment_adverse_media = models.BooleanField(default=False)
    riskassessment_beneficial_owner_checked = models.BooleanField(default=False)
    riskassessment_riskgrading_done = models.BooleanField(default=False)
    riskassessment_other_doc_obtained = models.CharField(max_length=100,default=None,null=True, blank=True)
    riskassessment_risk_type = models.CharField(max_length=100,default=None,null=True, blank=True)
    riskassessment_risk_score = models.PositiveIntegerField(default=0)
    riskassessment_sof_verified = models.BooleanField(default=False)
    riskassessment_review_of_profile_done = models.BooleanField(default=False)
    riskassessment_review_of_profile_date = models.CharField(max_length=50,default=None,null=True, blank=True)
    riskassessment_deposit_history = models.PositiveIntegerField(default=0)
    riskassessment_withdraw_history = models.PositiveIntegerField(default=0)
    riskassessment_is_transaction_pattern_usual = models.BooleanField(default=False)
    riskassessment_pep_approval = models.BooleanField(default=False)
    riskassessment_pep_facetoface_interview = models.BooleanField(default=False)

class BranchRelatedInfo(models.Model):
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,null=True, blank=True, related_name='branch_related_info')
    bank_account = models.ForeignKey(CustomerAccount,on_delete=models.CASCADE,null=True, blank=True, related_name='branch_related_info')
    branchrelated_completed_aof = models.BooleanField(default=0)
    branchrelated_wlc_false_positive = models.BooleanField(default=0)
    branchrelated_wlc_positive = models.BooleanField(default=0)
    branchrelated_wlc_checked = models.BooleanField(default=0)
    branchrelated_marketed_by_official = models.BooleanField(default=0)
    branchrelated_marketed_by_dsa = models.BooleanField(default=0)
    branchrelated_sector_code = models.CharField(max_length=20,default=None,null=True, blank=True)
    branchrelated_official_dsa_name = models.CharField(max_length=100,default=None,null=True, blank=True)
    branchrelated_employee_dsa_code = models.CharField(max_length=50,default=None,null=True, blank=True)
    branchrelated_acc_opening_officer_name = models.CharField(max_length=50,default=None,null=True, blank=True)
    branchrelated_acc_opening_approach_by_name = models.CharField(max_length=50,default=None,null=True, blank=True)
    branchrelated_acc_opening_officer_eid = models.CharField(max_length=50,default=None,null=True, blank=True)
    branchrelated_acc_opening_approach_by_eid = models.CharField(max_length=50,default=None,null=True, blank=True)
    branchrelated_address_verified = models.BooleanField(default=0)
    branchrelated_address_verification_method = models.CharField(max_length=100,default=None,null=True, blank=True)
    branchrelated_address_verifier_name = models.CharField(max_length=100,default=None,null=True, blank=True)
    branchrelated_address_verifier_eid = models.CharField(max_length=100,default=None,null=True, blank=True)
    branchrelated_certifying_officer_name = models.CharField(max_length=100,default=None,null=True, blank=True)
    branchrelated_certifying_officer_eid = models.CharField(max_length=100,default=None,null=True, blank=True)

class Introducer(models.Model):
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,null=True, blank=True, related_name='introducer')
    introducer_name = models.CharField(max_length=100,default=None,null=True, blank=True)
    introducer_dob = models.CharField(max_length=50,default=None,null=True, blank=True)
    introducer_mobile_no = models.CharField(max_length=50,default=None,null=True, blank=True)
    introducer_account_no = models.CharField(max_length=100,default=None,null=True, blank=True)
    introducer_id_type = models.CharField(max_length=50,default=None,null=True, blank=True)
    introducer_id_number = models.CharField(max_length=100,default=None,null=True, blank=True)

    def is_empty(self):
        status = self.introducer_name or self.introducer_dob or self.introducer_mobile_no or self.introducer_mobile_no \
            or self.introducer_id_number
        return False if status else True

class OtherBank(models.Model):
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,null=True, blank=True, related_name='other_bank')
    otherbank_index = models.SmallIntegerField(default=0)
    otherbank_name = models.CharField(max_length=100,default=None,null=True, blank=True)
    otherbank_branch = models.CharField(max_length=100,default=None,null=True, blank=True)
    otherbank_account_number = models.CharField(max_length=100,default=None,null=True, blank=True)

    def is_empty(self):
        status = self.otherbank_name or self.otherbank_branch or self.otherbank_account_number
        return False if status else True
    
class OtherBankCard(models.Model):
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,null=True, blank=True, related_name='other_bank_card')
    otherbankcard_index = models.SmallIntegerField(default=0)
    otherbankcard_name = models.CharField(max_length=100,default=None,null=True, blank=True)
    otherbankcard_card_number = models.CharField(max_length=100,default=None,null=True, blank=True)

    def is_empty(self):
        status = self.otherbankcard_name or self.otherbankcard_card_number
        return False if status else True


    
class CustomerOtherInfo(models.Model):
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,null=True, blank=True, related_name='otherinfo')
    info_key = models.CharField(max_length=100,default=None,null=True, blank=True)
    info_value = models.CharField(max_length=200,default=None,null=True, blank=True)



