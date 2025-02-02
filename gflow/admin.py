from django.contrib import admin
from .models import GFlowCollection, GFlowPage, GFlowApp

class GFlowCollectionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in GFlowCollection._meta.fields]
    filter_horizontal = ('pages',) 
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['modified']
        else:
            return ['modified']

class GFlowPageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in GFlowPage._meta.fields if field.name != 'content']
    save_as = True
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['name','modified']
        else:
            return ['modified']

class GFlowAppAdmin(admin.ModelAdmin):
    list_display = [field.name for field in GFlowApp._meta.fields]
    filter_horizontal = ('pages','collections') 
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['slug','modified']
        else:
            return ['modified']


admin.site.register(GFlowApp,GFlowAppAdmin)
admin.site.register(GFlowCollection,GFlowCollectionAdmin)
admin.site.register(GFlowPage,GFlowPageAdmin)