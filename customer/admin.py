from django.contrib import admin
from .models import CustomerProfile, CustomerVerificationScores, CustomerAccount
# Register your models here.


class CustomerAccountAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CustomerAccount._meta.fields]

class CustomerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CustomerProfile._meta.fields]

class CustomerScoresAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CustomerVerificationScores._meta.fields]


admin.site.register(CustomerAccount,CustomerAccountAdmin)
admin.site.register(CustomerProfile,CustomerAdmin)
admin.site.register(CustomerVerificationScores,CustomerScoresAdmin)