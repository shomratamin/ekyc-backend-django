from .models import BankSetting
from .serializers import BankSettingsSerializer

global bank_settings
bank_settings = dict()

def update_bank_settings(bank):
    global bank_settings
    _bank_settings = BankSetting.objects.filter(bank=bank)
    bank_settings[bank.slug] = BankSettingsSerializer(_bank_settings).data

def get_bank_settings(bank):
    global bank_settings
    if bank.slug is not None and bank.slug not in bank_settings:
        update_bank_settings(bank)
        print('update', bank_settings)
    print('return', bank_settings)
    return bank_settings[bank.slug]