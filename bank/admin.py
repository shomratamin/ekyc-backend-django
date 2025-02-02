from django.contrib import admin
from .models import BankSetting, CBSRequestLog



class CBSRequestLogAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CBSRequestLog._meta.fields]


admin.site.register(CBSRequestLog,CBSRequestLogAdmin)