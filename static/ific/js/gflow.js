var form_rule_set = {
    'customer_profile.nid_no': [],
    'customer_profile.id_type': [],
    'customer_profile.dob': [],
    'customer_profile.customer_name_eng': ['required', 'allow_text_only', 'to_capitalize'],
    'customer_profile.customer_name_ben': ['required', 'allow_text_only'],
    'customer_profile.father_name_eng': ['required', 'allow_text_only', 'to_capitalize'],
    'customer_profile.father_name_ben': ['required', 'allow_text_only'],
    'customer_profile.mother_name_eng': ['required', 'allow_text_only', 'to_capitalize'],
    'customer_profile.mother_name_ben': ['required', 'allow_text_only'],
    'customer_profile.spouse_name_eng': ['allow_text_only', 'to_capitalize'],
    'customer_profile.spouse_name_ben': ['allow_text_only'],
    'customer_profile.gender': [],
    'customer_profile.pres_address_eng': ['required', 'to_capitalize'],
    'customer_profile.pres_address_ben': [],
    'customer_profile.perm_address_eng': ['required', 'to_capitalize'],
    'customer_profile.perm_address_ben': [],
    'customer_profile.prof_address_eng': ['required', 'to_capitalize'],
    'customer_profile.prof_address_ben': [],
    'customer_profile.mailing_address': [],
    'customer_profile.tin_number': [],
    'customer_profile.etin_number': ['length=[12,12]', 'error-message=E-TIN number must be 12 digits long'],
    'customer_profile.nid_front_image': [],
    'customer_profile.nid_back_image': [],
    'customer_profile.customer_photo_from_card_image': [],
    'customer_profile.customer_photo_from_app_image': [],
    'customer_profile.customer_photo_other_from_app_image': [],
    'customer_profile.profession': ['required'],
    'customer_profile.other_profession': ['validate-if-empty=true', 'required-if-selected=selected__profession__Others'],
    'customer_profile.mobile_number': ['required', 'mobile-number-with-zero', 'allow_number_only'],
    'customer_profile.email': ['email'],
    'customer_profile.religion': [],
    'customer_profile.place_of_birth': [],
    'customer_profile.country_of_birth': [],
    'customer_profile.source_of_fund': ['required'],
    'customer_profile.other_source_of_fund': ['validate-if-empty=true', 'required-if-selected=selected__source_of_fund__Others'],
    'customer_profile.nature_of_business': [],
    'customer_profile.native_resident': [],
    'customer_profile.residential_status': [],
    'customer_profile.transaction_limit_monthly': [],
    'customer_profile.nationality': [],
    'customer_profile.monthly_income': ['allow_currency_only'],
    'customer_profile.us_residency': [],
    'customer_profile.us_citizenship': [],
    'customer_profile.us_pr_card': [],
    'customer_profile.us_have_residence_address': [],
    'customer_profile.us_have_correspondence_address': [],
    'customer_profile.us_address': [],
    'customer_profile.us_social_security_number': ['validate-if-empty=true', 'required-if-yes=checked__us_citizenship__or__us_pr_card'],
    'customer_profile.us_contact_number': ['validate-if-empty=true', 'required-if-yes=checked__us_have_correspondence_address', 'allow_number_only'],
    'customer_profile.nrf_reason_for_acc_opening': ['validate-if-empty=true', 'minlength=10', 'maxlength=500', 'required-if-not-selected=selected__residential_status__Resident Bangladeshi'],
    'customer_profile.nrf_type_of_visa_resident': [],
    'customer_profile.nrf_type_of_visa_work': [],
    'customer_profile.nrf_visa_validity_upto': ['validate-if-empty=true', 'required-if-not-selected=selected__residential_status__Resident Bangladeshi'],
    'customer_profile.nrf_work_permit_letter_obtained': [],
    'customer_profile.preferred_branch': [],
    'additional_services.cheque_book': [],
    'additional_services.debit_card': [],
    'additional_services.sms_alert': [],
    'additional_services.digital_banking': [],
    'additional_services.e_statement_facility': [],
    'bank_account.branch_code': [],
    'bank_account.account_type': ['required'],
    'bank_account.account_operation_type': ['required'],
    'bank_account.account_profile_type': ['required'],
    'bank_account.account_name': [],
    'bank_account.account_number': ['length=[2,16]', 'allow_number_only'],
    'bank_account.unique_account_number': [],
    'bank_account.transaction_amount_monthly': [],
    'bank_account.account_remarks': [],
    'bank_account.initial_deposit': ['required', 'min=10','allow_number_only'],
    'bank_account.initial_deposit_text': ['pattern=^[a-zA-Z ]+$'],
    'bank_account.preferred_currency': [],
    'bank_account.joint_mode_of_operation': [],
    'bank_account.joint_signatory': [],
    'bank_account.joint_signatory_other': [],
    'bank_account.joint_number_of_applicants': [],
    'bank_account.joint_account_title_eng': [],
    'bank_account.joint_account_title_ben': [],
    'bank_account.joint_second_applicant': [],
    'bank_account.joint_third_applicant': [],
    'bank_account.joint_fourth_applicant': [],
    'bank_account.joint_fifth_applicant': [],
    'transaction_profile.transaction_channel_index': ['allow_number_only'],
    'transaction_profile.transaction_channel': [],
    'transaction_profile.transaction_deposit_number': ['allow_number_only'],
    'transaction_profile.transaction_deposit_amount': ['allow_number_only'],
    'transaction_profile.transaction_deposit_amount_per_max': ['allow_number_only'],
    'transaction_profile.transaction_withdraw_number': ['allow_number_only'],
    'transaction_profile.transaction_withdraw_amount': ['allow_number_only'],
    'transaction_profile.transaction_withdraw_amount_per_max': ['allow_number_only'],
    'risk_grading.riskgrading_type_of_onboarding': [],
    'risk_grading.riskgrading_geographic_risk': [],
    'risk_grading.riskgrading_is_pep': [],
    'risk_grading.riskgrading_is_ip': [],
    'risk_grading.riskgrading_is_pep_family': [],
    'risk_grading.riskgrading_product_and_channel_risk': [],
    'risk_grading.riskgrading_business_and_activity_risk': [],
    'risk_grading.riskgrading_businsess_or_profession': [],
    'risk_grading.riskgrading_transaction_risk': [],
    'risk_grading.riskgrading_credible_source_of_fund': [],
    'risk_grading.riskgrading_client_citizenship_ust': [],
    'risk_grading.riskgrading_donates_to_pep': [],
    'risk_assessment.riskassessment_unscrs_check_done': [],
    'risk_assessment.riskassessment_is_pep': [],
    'risk_assessment.riskassessment_pep_details': [],
    'risk_assessment.riskassessment_adverse_media': [],
    'risk_assessment.riskassessment_beneficial_owner_checked': [],
    'risk_assessment.riskassessment_riskgrading_done': [],
    'risk_assessment.riskassessment_other_doc_obtained': ['allow_text_only', 'to_capitalize'],
    'risk_assessment.riskassessment_risk_type': [],
    'risk_assessment.riskassessment_risk_score': [],
    'risk_assessment.riskassessment_sof_verified': [],
    'risk_assessment.riskassessment_review_of_profile_done': [],
    'risk_assessment.riskassessment_review_of_profile_date': [],
    'risk_assessment.riskassessment_deposit_history': [],
    'risk_assessment.riskassessment_withdraw_history': [],
    'risk_assessment.riskassessment_is_transaction_pattern_usual': [],
    'risk_assessment.riskassessment_pep_approval': [],
    'risk_assessment.riskassessment_pep_facetoface_interview': [],
    'branch_related_info.branchrelated_completed_aof': ['required'],
    'branch_related_info.branchrelated_wlc_false_positive': ['required'],
    'branch_related_info.branchrelated_wlc_positive': [],
    'branch_related_info.branchrelated_marketed_by_official': [],
    'branch_related_info.branchrelated_marketed_by_dsa': [],
    'branch_related_info.branchrelated_sector_code': ['required', 'length=[6,6]', 'allow_number_only', 'error-message=This value must be 6 digits long'],
    'branch_related_info.branchrelated_official_dsa_name': ['required', 'allow_text_only', 'to_capitalize'],
    'branch_related_info.branchrelated_employee_dsa_code': ['required', 'allow_alphanum_only'],
    'branch_related_info.branchrelated_acc_opening_officer_name': ['required', 'allow_text_only', 'to_capitalize'],
    'branch_related_info.branchrelated_acc_opening_approach_by_name': ['required', 'allow_text_only', 'to_capitalize'],
    'branch_related_info.branchrelated_acc_opening_officer_eid': ['required', 'allow_alphanum_only'],
    'branch_related_info.branchrelated_acc_opening_approach_by_eid': ['required', 'allow_alphanum_only'],
    'branch_related_info.branchrelated_address_verified': ['required'],
    'branch_related_info.branchrelated_address_verification_method': [],
    'branch_related_info.branchrelated_address_verifier_name': ['required', 'allow_text_only', 'to_capitalize'],
    'branch_related_info.branchrelated_address_verifier_eid': ['required', 'allow_alphanum_only'],
    'branch_related_info.branchrelated_certifying_officer_name': ['required', 'allow_text_only', 'to_capitalize'],
    'branch_related_info.branchrelated_certifying_officer_eid': ['required', 'allow_alphanum_only'],
    'introducer.introducer_name': ['allow_text_only', 'to_capitalize'],
    'introducer.introducer_dob': ['required-minimum-age=valueof__introducer_dob__18'],
    'introducer.introducer_mobile_no': ['mobile-number-bangladesh', 'allow_number_only'],
    'introducer.introducer_account_no': ['length=[1,13]', 'allow_number_only', 'error-message=This value length is invalid. It should be between 1 and 13 digits long.'],
    'introducer.introducer_id_type': [],
    'introducer.introducer_id_number': ['allow_number_only', 'length=[1,17]', 'error-message=This value length is invalid. It should be between 1 and 17 digits long.'],
    'other_banks.otherbank_index': [],
    'other_banks.otherbank_name': [],
    'other_banks.otherbank_branch': ['allow_text_only', 'to_capitalize'],
    'other_banks.otherbank_account_number': ['validate-if-empty=true', 'required-if-not-empty=selectedvalueof__otherbank_name', 'allow_number_only', 'length=[1,16]', 'error-message=This value length is invalid. It should be between 1 and 16 digits long.'],
    'other_bank_cards.otherbankcard_index': [],
    'other_bank_cards.otherbankcard_name': ['allow_text_only', 'to_capitalize'],
    'other_bank_cards.otherbankcard_card_number': ['validate-if-empty=true', 'required-if-not-empty=selectedvalueof__otherbankcard_name', 'creditcard'],
    'nominees.nominee_index': [],
    'nominees.nominee_name_eng': ['required', 'allow_text_only', 'to_capitalize'],
    'nominees.nominee_name_ben': ['allow_text_only'],
    'nominees.nominee_dob': ['required', 'future-date-not-allowed'],
    'nominees.nominee_relation': ['required', 'allow_text_only', 'to_capitalize', 'error-message=Plese specify your relationship with nominee.'],
    'nominees.nominee_pres_address_eng': ['required', 'to_capitalize'],
    'nominees.nominee_perm_address_eng': ['required', 'to_capitalize'],
    'nominees.nominee_pres_address_ben': [],
    'nominees.nominee_perm_address_ben': [],
    'nominees.nominee_share_percentage': ['required', 'allow_number_only', 'sum-equals=allvaluesof__nominee_share_percentage__100'],
    'nominees.nominee_id_type': [],
    'nominees.nominee_id_number': ['required', 'id-type=selectedvalueof__nominee_id_type'],
    'nominees.nominee_id_front_image': ['validate-if-empty=true', 'required-if-age-greater-than=valueof__nominee_dob__18'],
    'nominees.nominee_id_back_image': ['validate-if-empty=true', 'required-if-age-greater-than=valueof__nominee_dob__18'],
    'nominees.nominee_photo_image': ['required'],
    'nominees.nominee_tin_number': ['allow_number_only'],
    'nominees.nominee_account_number': ['length=[1,13]', 'error-message=This value length is invalid. It should be between 1 and 13 digit long.'],
    'nominees.nominee_minor': [],
    'nominees.nominee_minor_legal_guardian_name': ['to_capitalize', 'validate-if-empty=true', 'required-if-age-less-than=valueof__nominee_dob__18', 'allow_text_only'],
    'nominees.nominee_minor_legal_guardian_dob': ['validate-if-empty=true', 'required-minimum-age-if-age-less-than=valueof__nominee_dob__18'],
    'nominees.nominee_minor_legal_guardian_pres_address_eng': ['validate-if-empty=true', 'required-if-age-less-than=valueof__nominee_dob__18', 'to_capitalize'],
    'nominees.nominee_minor_legal_guardian_pres_address_ben': [],
    'nominees.nominee_minor_legal_guardian_perm_address_eng': ['validate-if-empty=true', 'required-if-age-less-than=valueof__nominee_dob__18', 'to_capitalize'],
    'nominees.nominee_minor_legal_guardian_perm_address_ben': [],
    'nominees.nominee_minor_legal_guardian_relation': ['allow_text_only', 'to_capitalize', 'validate-if-empty=true', 'required-if-age-less-than=valueof__nominee_dob__18', 'allow_text_only'],
    'nominees.nominee_minor_legal_guardian_contact_no': ['allow_number_only', 'mobile-number-with-zero-required-if-age-less-than=valueof__nominee_dob__18', 'validate-if-empty=true'],
    'nominees.nominee_minor_legal_guardian_id_type': [],
    'nominees.nominee_minor_legal_guardian_photo_image': ['validate-if-empty=true', 'required-if-age-less-than=valueof__nominee_dob__18'],
    'nominees.nominee_minor_legal_guardian_id_front_image': ['validate-if-empty=true', 'required-if-age-less-than=valueof__nominee_dob__18'],
    'nominees.nominee_minor_legal_guardian_id_back_image': ['validate-if-empty=true', 'required-if-age-less-than=valueof__nominee_dob__18'],
    'nominees.nominee_minor_legal_guardian_id_number': ['validate-if-empty=true', 'required-id-type-if-age-less-than=valueofandselected__nominee_dob__or__nominee_minor_legal_guardian_id_type'],
}

var form_rule_set_map = {}
for (let key in form_rule_set) {
    let rules = form_rule_set[key]
    let field = key.split('.')[1]
    form_rule_set_map[field] = rules
}

String.prototype.capitalize_first_letter = function () {
    return this.charAt(0).toUpperCase() + this.slice(1)
}

function bind_validator() {
    let prefix = 'data-parsley-'
    $('input, textarea').each(function (index) {
        let name_r = this.name
        let suffix = ''
        if (name_r.endsWith(']')) {
            let splits = name_r.split('[')
            name_r = splits[0]
            if (splits.length == 2) {
                suffix = '[' + splits[1]
            }
            else if (splits.length == 3) {
                suffix = '[' + splits[1] + '[' + splits[2]
            }
        }
        if (name_r.endsWith('_base64')) {
            name_r = name_r.replace('_base64', '')
            // suffix = '_base64' + suffix
            console.log('suffix', suffix)
        }
        let rules = form_rule_set_map[name_r]
        if (typeof rules != 'undefined') {
            for (let i = 0; i < rules.length; i++) {
                let rule = rules[i]
                let rule_value = rule.split('=')
                let _rule = ''
                let _rule_value = ''
                if (rule_value.length > 1) {
                    _rule = rule_value[0]
                    _rule_value = rule_value[1]
                }
                else {
                    _rule = rule_value[0]
                }

                if (_rule.includes('_')) {
                    $(this).addClass(_rule)
                }
                else {
                    if (_rule_value == 'this') {
                        _rule_value = this.name
                    }
                    if (_rule_value.startsWith('checked__')) {
                        _rule_value = _rule_value.replace('checked__', '')
                        if (_rule_value.includes('__or__')) {
                            let _rule_values = _rule_value.split('__or__')
                            for (let j = 0; j < _rule_values.length; j++) {
                                _rule_values[j] = `input[name="${_rule_values[j] + suffix}"]:checked`
                            }
                            _rule_value = _rule_values
                        }
                        else {
                            _rule_value = `input[name="${_rule_value + suffix}"]:checked`
                        }
                    }
                    else if (_rule_value.startsWith('selected__')) {
                        _rule_value = _rule_value.replace('selected__', '')

                        let name_value = _rule_value.split('__')

                        _rule_value = `select[name="${name_value[0] + suffix}"] option:selected` + '__' + name_value[1]

                    }
                    else if (_rule_value.startsWith('allvaluesof__')) {
                        _rule_value = _rule_value.replace('allvaluesof__', '')

                        let name_value = _rule_value.split('__')

                        _rule_value = `input[name^="${name_value[0]}"]` + '__' + name_value[1]

                    }
                    else if (_rule_value.startsWith('selectedvalueof__')) {
                        _rule_value = _rule_value.replace('selectedvalueof__', '')
                        if (_rule_value.includes('__or__')) {
                            let _rule_values = _rule_value.split('__or__')
                            for (let j = 0; j < _rule_values.length; j++) {
                                _rule_values[j] = `select[name="${_rule_values[j] + suffix}"] option:selected`
                            }
                            _rule_value = _rule_values
                        }
                        else {
                            _rule_value = `select[name="${_rule_value + suffix}"] option:selected`
                        }
                    }
                    else if (_rule_value.startsWith('valueofandselected__')) {
                        _rule_value = _rule_value.replace('valueofandselected__', '')
                        if (_rule_value.includes('__or__')) {
                            let _rule_values = _rule_value.split('__or__')
                            _rule_values[0] = `input[name="${_rule_values[0] + suffix}"]`
                            _rule_values[1] = `select[name="${_rule_values[1] + suffix}"] option:selected`

                            _rule_value = _rule_values
                        }
                        else {
                            _rule_value = `select[name="${_rule_value + suffix}"] option:selected`
                        }
                    }
                    else if (_rule_value.startsWith('valueof__')) {
                        _rule_value = _rule_value.replace('valueof__', '')

                        let name_value = _rule_value.split('__')
                        if (name_value.length == 1) {
                            _rule_value = `input[name="${name_value[0] + suffix}"]`
                            console.log('rule value', _rule_value)
                        }
                        else if (name_value.length == 2) {
                            _rule_value = `input[name="${name_value[0] + suffix}"]` + '__' + name_value[1]
                            console.log('rule value', _rule_value)
                        }

                    }


                    _rule = prefix + _rule
                    $(this).attr(_rule, _rule_value)
                }
            }
        }
    })

    validator = $('form').parsley({ 'trigger': 'input blur' });
    if (typeof validator != 'undefined') {
        window.gflow_validator = validator
        window.gflow_validator.validate()
    }
    $('#wrapper').delegate('.allow_number_only', 'keypress', function (evt) {
        if (evt.which != 8 && evt.which != 0 && evt.which < 48 || evt.which > 57) {
            evt.preventDefault();
        }
    })
    $('#wrapper').delegate('.allow_number_only', 'change, keyup', function (evt) {
        let value = $(this).val()
        if (value < 0) {
            $(this).val('')
        }
    })

    $('#wrapper').delegate('.allow_currency_only', 'keypress', function (evt) {
        if (evt.which != 8 && evt.which != 0 && evt.which != 44 && evt.which < 48 || evt.which > 57) {
            evt.preventDefault();
        }
    })
    // $('#wrapper').delegate('.allow_currency_only', 'change', function (evt) {
    //     let value = $(this).val()
    //     console.log(value)
    //     if( value.length > 0){
    //     value = value.replace(',','')
    //     value = Number(value).toLocaleString('en')
    //     $(this).val(value)
    //     }
    // })




    $('#wrapper').delegate('.to_capitalize', 'keyup', function (evt) {
        let value = $(this).val()
        let values = value.split(' ')
        let final_value = ''
        for (let i = 0; i < values.length; i++) {
            let _value = values[i]
            _value = _value.capitalize_first_letter()
            if (i == 0) {
                final_value = final_value + _value
            }
            else {
                final_value = final_value + ' ' + _value
            }
        }
        $(this).val(final_value)
    })

    $('#wrapper').delegate('select[name="account_type"],select[name="account_type_bankside"], select[name="preferred_branch_code"]', 'change', function (evt) {
        window.gflow_validator.validate()
    })
    $('#wrapper').delegate('input[name^="nominee_minor_legal_guardian_dob"]', 'change', function (evt) {
        window.gflow_validator.validate()
    })

    $('#wrapper').delegate('.allow_text_only', 'keypress', function (evt) {
        let block_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        block_list.forEach(function (digit) {
            if (digit == String.fromCharCode(evt.which) && evt.which != 32) {
                evt.preventDefault()
            }
        })
    })

    $('#wrapper').delegate('.allow_alphanum_only', 'keypress', function (evt) {

        if (!(evt.which > 47 && evt.which < 58) && // numeric (0-9)
            !(evt.which > 64 && evt.which < 91) && // upper alpha (A-Z)
            !(evt.which > 96 && evt.which < 123)) { // lower alpha (a-z)
            evt.preventDefault();
        }

    })
}

$(document).ready(function () {
    bind_validator()
})