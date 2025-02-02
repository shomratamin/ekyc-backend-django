from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import User
from django.contrib.auth.models import Group

class MyUserAdmin(UserAdmin):
    def get_form(self, request, obj=None, **kwargs):
        # Get form from original UserAdmin.
        form = super(MyUserAdmin, self).get_form(request, obj, **kwargs)
        # if 'user_permissions' in form.base_fields:
        #     permissions = form.base_fields['user_permissions']
        #     permissions.queryset = permissions.queryset.filter(content_type__name='log entry')
        return form

admin.site.register(User, MyUserAdmin)


class GroupAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('permissions',)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'permissions':
            qs = kwargs.get('queryset', db_field.remote_field.model.objects)
            # Avoid a major performance hit resolving permission names which
            # triggers a content_type load:
            kwargs['queryset'] = qs.select_related('content_type')
        return super().formfield_for_manytomany(db_field, request=request, **kwargs)

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
