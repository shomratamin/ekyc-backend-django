import requests
import sys
import csv


with open('users.csv',mode='r', encoding='utf-8') as csvfile:
    user_list = csv.reader(csvfile)

    for _user in user_list:
        auth_token = sys.argv[1]
        data = dict()
        data['mobile_no'] = _user[3]
        data['branch_code'] = _user[4]
        data['email'] = _user[2].lower()
        data['name'] = _user[1]
        response = requests.post('https://idigitalaof.ificbankbd.com/bank/agents/',data= data, headers={'Authorization': 'Token ' + auth_token})
        print(response.text)