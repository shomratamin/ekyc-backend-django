from .models import CBSRequestLog
import requests
import string


class CBS:
    def __init__(self):
        super().__init__()
        self.request_id = None

    def get(self, url, req_headers = {}, data = {}, data_type='text', timeout=30):
        if data_type == 'json':
            response = requests.get(url, json=data, headers= req_headers, timeout= timeout)
        else:
            response = requests.get(url, data=data, headers= req_headers, timeout= timeout)

        return response

    def post(self, url, req_headers = {}, data = {}, data_type='text', timeout=30):
        if data_type == 'json':
            response = requests.post(url, json=data, headers= req_headers, timeout= timeout)
        else:
            response = requests.post(url, data=data, headers= req_headers, timeout= timeout)

        return response

    def put(self):
        pass

    def delete(self):
        pass

    def generate_request_id(self):
        pass

    def get_request_id(self):
        return self.request_id