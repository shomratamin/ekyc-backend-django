from rest_framework import permissions
from .models import User
from rest_framework.permissions import IsAuthenticated
from rest_condition import And, Or, Not


class AllowAnyGflow(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

class IsSuperAdmin(permissions.BasePermission):
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        return User.USER_TYPES_MAP['superadmin'] == request.user.user_type

class IsAdmin(permissions.BasePermission):
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        return User.USER_TYPES_MAP['admin'] == request.user.user_type

class IsBank(permissions.BasePermission):
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        return User.USER_TYPES_MAP['bank'] == request.user.user_type

class IsAgent(permissions.BasePermission):
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        return User.USER_TYPES_MAP['agent'] == request.user.user_type

class IsCustomer(permissions.BasePermission):
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        return User.USER_TYPES_MAP['customer'] == request.user.user_type

class IsGet(permissions.BasePermission):
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):

        return request.method == 'GET'

class IsPost(permissions.BasePermission):
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):

        return request.method == 'POST'
    
class IsDelete(permissions.BasePermission):
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):

        return request.method == 'DELETE'

class IsPut(permissions.BasePermission):
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):

        return request.method == 'PUT'