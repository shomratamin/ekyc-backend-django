from collections import OrderedDict
import json
import requests
from django.conf import settings

def add_risk_grading_item(group_key, sub_group_key, item_value):
    data = OrderedDict()
    data['RGGroupKey'] = group_key
    data['RGSubGroupKey'] = sub_group_key
    data['RGItem'] = item_value
    return data

def map_risk_grading_data(dictionary , key, value):
    _item = False
    yes_no = 'No'
    if value == 1 or value == '1':
        yes_no = "Yes"
    if key == 'riskgrading_type_of_onboarding' :
        _item = add_risk_grading_item('TypeOfOnBoarding','', value)
    
    elif key == 'riskgrading_geographic_risk':
        _item = add_risk_grading_item('GeographicRisk','', value)
        
    elif key == 'riskgrading_client_citizenship_ust':

        _item = add_risk_grading_item('GeographicRisk','ForeignCitizen', yes_no)

    elif key == 'riskgrading_is_pep':
        _item = add_risk_grading_item('TypeOfCustomer','IsClientPEPOrChiefOrHighOfficialOfIntlOrg', yes_no)
        
    elif key == 'riskgrading_is_ip':
        _item = add_risk_grading_item('TypeOfCustomer','IsClientOrFamilyOrCloseAssociatesRelatedToIP', yes_no)
        
    elif key == 'riskgrading_is_pep_family':
        _item = add_risk_grading_item('TypeOfCustomer','IsFamilyOrCloseAssociatesPEPOrChiefOrHighOfficialOfIntlOrg', yes_no)

    #This is for BusinessRisk
    elif key == 'riskgrading_business_and_activity_risk':
        _item = add_risk_grading_item('BusinessAndActivityRisk','BusinessRisk', value)
        
    #This is for ProfessionalRisk
    elif key == 'riskgrading_profession_and_activity_risk':
        _item = add_risk_grading_item('BusinessAndActivityRisk','ProfessionalRisk', value) 

    elif key == 'riskgrading_product_and_channel_risk':
        _item = add_risk_grading_item('ProductAndChannelRisk','', value)  
 
    elif key == 'riskgrading_transaction_risk':
        _item = add_risk_grading_item('TransectionRisk','', value) 
        
    elif key == 'riskgrading_credible_source_of_fund':
        _item = add_risk_grading_item('TranspranceyRisk','', yes_no) 

    if _item:
        dictionary['BusinessData']['CustRiskGrading'].append(_item)

    return dictionary

def calculate_risk_grading(risk_grading_model):
    print('risk grading model is business or profession', risk_grading_model.riskgrading_businsess_or_profession)
    print('risk grading model business', risk_grading_model.riskgrading_business_and_activity_risk)
    print('risk grading model profession', risk_grading_model.riskgrading_profession_and_activity_risk)
    risk_data = OrderedDict()
    risk_data['BusinessData'] = OrderedDict()
    risk_data['BusinessData']['CustRiskGrading'] = []
    risk_data['BusinessData']['CustomerId'] = risk_grading_model.customer.id

    risk_data = map_risk_grading_data(risk_data, 'riskgrading_type_of_onboarding', risk_grading_model.riskgrading_type_of_onboarding)
    risk_data = map_risk_grading_data(risk_data, 'riskgrading_geographic_risk', risk_grading_model.riskgrading_geographic_risk)
    risk_data = map_risk_grading_data(risk_data, 'riskgrading_client_citizenship_ust', risk_grading_model.riskgrading_client_citizenship_ust)
    risk_data = map_risk_grading_data(risk_data, 'riskgrading_is_pep', risk_grading_model.riskgrading_is_pep)
    risk_data = map_risk_grading_data(risk_data, 'riskgrading_is_ip', risk_grading_model.riskgrading_is_ip)
    risk_data = map_risk_grading_data(risk_data, 'riskgrading_is_pep_family', risk_grading_model.riskgrading_is_pep_family)
    if risk_grading_model.riskgrading_businsess_or_profession == 'business':
        risk_data = map_risk_grading_data(risk_data, 'riskgrading_business_and_activity_risk', risk_grading_model.riskgrading_business_and_activity_risk)
        risk_data = map_risk_grading_data(risk_data, 'riskgrading_profession_and_activity_risk', '')
    elif risk_grading_model.riskgrading_businsess_or_profession == 'profession':
        risk_data = map_risk_grading_data(risk_data, 'riskgrading_profession_and_activity_risk', risk_grading_model.riskgrading_profession_and_activity_risk)
        risk_data = map_risk_grading_data(risk_data, 'riskgrading_business_and_activity_risk', '')
    risk_data = map_risk_grading_data(risk_data, 'riskgrading_product_and_channel_risk', risk_grading_model.riskgrading_product_and_channel_risk)
    risk_data = map_risk_grading_data(risk_data, 'riskgrading_transaction_risk', risk_grading_model.riskgrading_transaction_risk)
    risk_data = map_risk_grading_data(risk_data, 'riskgrading_credible_source_of_fund', risk_grading_model.riskgrading_credible_source_of_fund)

    risk_data_json = json.dumps(risk_data,ensure_ascii=False)

    print('request', risk_data_json)

    req_headers = {'Content-Type':'application/json; charset=utf-8', 'Connection':'keep-alive'}
    try:
        response = requests.post(settings.AML_SERVICE_BASE_URL, json=risk_data, headers=req_headers, timeout=10)
    except:
        return False

    return response.json()


def parse_and_save_risk_grading_scores(risk_grading_scores, aml_response_json):
    assessment_status = aml_response_json['responseCode']
    
    if assessment_status == 200:
        assessment_scores = aml_response_json['responseBusinessData']
        assessment_scores = json.loads(assessment_scores)
        assessment_scores_details = assessment_scores['RiskGradingCalculationDetails']

        for score in assessment_scores_details:
            if score['RGGroupKey'] == 'BusinessAndActivityRisk' and score['RGSubGroupKey'] == 'BusinessRisk':
                risk_grading_scores.riskgradingscore_business_and_activity_risk = score['Score']
                
            elif score['RGGroupKey'] == 'BusinessAndActivityRisk' and score['RGSubGroupKey'] == 'ProfessionalRisk':
                risk_grading_scores.riskgradingscore_profession_and_activity_risk = score['Score']
                
            elif score['RGGroupKey'] == 'GeographicRisk' and score['RGSubGroupKey'] == None:
                risk_grading_scores.riskgradingscore_geographic_risk = score['Score']
                
            elif score['RGGroupKey'] == 'GeographicRisk' and score['RGSubGroupKey'] == 'ForeignCitizen':
                risk_grading_scores.riskgradingscore_client_citizenship_ust = score['Score']  
                
            elif score['RGGroupKey'] == 'ProductAndChannelRisk' and score['RGSubGroupKey'] == None:
                risk_grading_scores.riskgradingscore_product_and_channel_risk = score['Score'] 
                
            elif score['RGGroupKey'] == 'TransectionRisk' and score['RGSubGroupKey'] == None:
                risk_grading_scores.riskgradingscore_transaction_risk = score['Score'] 
                
            elif score['RGGroupKey'] == 'TranspranceyRisk' and score['RGSubGroupKey'] == None:
                risk_grading_scores.riskgradingscore_credible_source_of_fund = score['Score'] 
                
            elif score['RGGroupKey'] == 'TypeOfCustomer' and score['RGSubGroupKey'] == 'IsClientOrFamilyOrCloseAssociatesRelatedToIP':
                risk_grading_scores.riskgradingscore_is_ip = score['Score'] 
                
            elif score['RGGroupKey'] == 'TypeOfCustomer' and score['RGSubGroupKey'] == 'IsClientPEPOrChiefOrHighOfficialOfIntlOrg':
                risk_grading_scores.riskgradingscore_is_pep = score['Score'] 
                
            elif score['RGGroupKey'] == 'TypeOfCustomer' and score['RGSubGroupKey'] == 'IsFamilyOrCloseAssociatesPEPOrChiefOrHighOfficialOfIntlOrg':
                risk_grading_scores.riskgradingscore_is_pep_family = score['Score'] 
                
            elif score['RGGroupKey'] == 'TypeOfOnBoarding' and score['RGSubGroupKey'] == None:
                risk_grading_scores.riskgradingscore_type_of_onboarding = score['Score']

                

        risk_grading_scores.riskgradingscore_score = assessment_scores['RiskGradingScore']
        risk_grading_scores.riskgradingscore_assessment_type = assessment_scores['RiskGradingAssesment']
        risk_grading_scores.save()
    return True
    