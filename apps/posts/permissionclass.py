from rest_framework.permissions import BasePermission

class PostPermissionRead(BasePermission):

    def has_object_permission(self, request, view, obj):
        postpermissioncategory=obj.postinverse.all()
        permissiondict={i.category.category_name:i.permission.permission_name for i in postpermissioncategory}
        team=obj.author.team
        user=request.user
        if user==obj.author and permissiondict.get('AUTHOR')=='NONE':
            return False
        elif user==obj.author and (permissiondict.get('AUTHOR')=='EDIT'or permissiondict.get('AUTHOR')=='READ_ONLY' ):
            return True
        if team==user.team and permissiondict.get('TEAM')=='NONE':
            return False
        elif user.team==team and (permissiondict.get('TEAM')=='EDIT'or permissiondict.get('TEAM')=='READ_ONLY' ):
            return True
        if user.is_authenticated and permissiondict.get('AUTHENTICATED')=='NONE':
            return False
        elif user.is_authenticated and (permissiondict.get('AUTHENTICATED')=='EDIT'or permissiondict.get('AUTHENTICATED')=='READ_ONLY' ):
            return True
        if (not user.is_authenticated) and permissiondict.get('PUBLIC')=='NONE':
            return False
        elif (not user.is_authenticated) and (permissiondict.get('PUBLIC')=='EDIT'or permissiondict.get('PUBLIC')=='READ_ONLY' ):
            return True
        return False
    
class PostPermissionEdit(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return True