from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    # def has_permission(self, request, view):
    #     print('fgfgff')
    #     return request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        is_owner = request.user == obj.user
        is_super_user = request.user.is_superuser or request.user.is_staff
        return is_owner or is_super_user
