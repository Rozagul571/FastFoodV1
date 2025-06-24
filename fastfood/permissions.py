# from rest_framework import permissions
#
# from users.models import User
#
# class IsAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role == User.RoleType.ADMIN
#
# class IsWaiterOrAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role in [User.RoleType.ADMIN, User.RoleType.WAITER]
#
# class IsUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role == User.RoleType.USER

from rest_framework import permissions
class Permissions(permissions.BasePermission):
    def has_permission(self, request, view):
        view_name = view.__class__.__name__.lower()
        if 'order' in view_name:
            view_basename = 'order'
        elif 'dish' in view_name:
            view_basename = 'dish'
        elif 'category' in view_name:
            view_basename = 'category'
        elif 'restaurant' in view_name:
            view_basename = 'restaurant'
        elif 'user' in view_name or 'register' in view_name:
            view_basename = 'register'
        else:
            view_basename = ''
        print(f"User: {request.user}, Autentifikatsiya: {request.user.is_authenticated}, Method: {request.method}, View: {view_basename}")

        if view_basename in ['dish', 'category', 'restaurant'] and request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        if view_basename == 'register':
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role == 'admin':
            return True
        if request.user.role == 'waiter':
            if view_basename in ['dish', 'category', 'order'] and request.method not in ['GET', 'HEAD', 'OPTIONS']:
                restaurant_id = request.data.get('restaurant_id')
                if restaurant_id:
                    return request.user.restaurants.filter(id=restaurant_id).exists()
            return True
        if request.user.role == 'user':
            if view_basename in ['dish', 'category', 'restaurant'] and request.method in ['GET', 'HEAD', 'OPTIONS']:
                return True
            if view_basename == 'order' and request.method == 'POST':
                return True
            if view_basename == 'order' and request.method in ['GET', 'HEAD', 'OPTIONS']:
                return view.queryset.filter(user=request.user).exists()
            if view_basename == 'user' and request.method in ['GET', 'HEAD', 'OPTIONS']:
                return True
            return False
        return False