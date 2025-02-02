from django.db.models import Model, Q
from collections import OrderedDict



class QueryBuilder:
    def __init__(self, model, request, method = 'GET'):
        self.model = model
        self.request = request
        self.filter_method_from_request = method
        self.output_query = None
        self.__build_query()
        self.allowed_suffix = set([])

    def __extract_operator_query(self,key, fields):
        _operator = 'and'
        _key = key
        if key.startswith('or__'):
            _operator = 'or'
            _key = key[4:]

        if key.startswith('and__'):
            _operator = 'and'
            _key = key[5:]

        if key.startswith('not__'):
            _operator = 'not'
            _key = key[5:]

        __key = _key
        if '__' in _key:
            _k = _key.split('__')
            if len(_k) > 1:
                __key = _k[0]

        if not __key in fields:
            _operator = 'reject'

        return _operator, _key

    def __build_query(self):
        model_fields = set([f.name for f in self.model._meta.get_fields()])
        query_param_value = OrderedDict()
        if self.filter_method_from_request == 'GET' or self.filter_method_from_request == 'ALL':
            for key in self.request.GET:
                value = self.request.GET[key]
                if len(value) > 0:
                    query_param_value[key] = value

        if self.filter_method_from_request == 'POST' or self.filter_method_from_request == 'ALL':
            for key in self.request.POST:
                value = self.request.POST[key]
                if len(value) > 0:
                    query_param_value[key] = value

        _query = Q()
        for key, value in query_param_value.items():
            operator, query_key = self.__extract_operator_query(key, model_fields)
            if operator == 'and':
                _query.add(Q(**{query_key: value}), Q.AND)
            elif operator == 'or':
                _query.add(Q(**{query_key: value}), Q.OR) 
            elif operator == 'not':
                _query.add(~Q(**{query_key: value}), Q.AND)

        print(_query)

        self.output_query = _query
            


    def get_query(self):
        return self.output_query
