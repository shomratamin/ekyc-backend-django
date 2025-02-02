from django.core.signals import got_request_exception, request_started, request_finished, \
    setting_changed



def request_exception_handler(signal, sender, **kwargs):
    print('signal', signal)
    print('sender', sender)
    print('args', kwargs)


got_request_exception.connect(request_exception_handler)