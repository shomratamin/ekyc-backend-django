from django.db import models
from .bank import Bank
from .ecstatus import EcStatus

class KycDataSource(models.Model):
    ip_bank = models.CharField(max_length=28, blank=True, null = True)
    ip_ec = models.CharField(max_length=28)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    bank = models.ForeignKey(Bank,on_delete=models.CASCADE,to_field='slug')
    status = models.ForeignKey(EcStatus,on_delete=models.CASCADE, null=True, blank=True)
