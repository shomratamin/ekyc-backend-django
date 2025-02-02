from django.db import models
from .bank import Bank

class Branch(models.Model):
    name = models.CharField(max_length = 128)
    branch_index = models.IntegerField(default=0)
    address = models.CharField(max_length = 500, blank=True, null = True)
    bank = models.ForeignKey(Bank,on_delete=models.CASCADE,to_field='slug')
    code = models.CharField(max_length=50, default=' ')
    district = models.CharField(max_length=100, default=' ')
    division = models.CharField(max_length=100, default=' ')
    visible_in_form = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)