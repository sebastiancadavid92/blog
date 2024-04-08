from django.contrib import admin
from  .models import User,Team
from django.contrib.auth.models import Group




class UserAdmin(admin.ModelAdmin):
    # Lista de campos que deseas excluir
    exclude = ['is_staff','is_active', 'last_login','user_permissions','groups','is_superuser']

class UserInline(admin.TabularInline):
    model = User
    extra = 0
    exclude= ['is_staff','is_active', 'last_login','user_permissions','groups','is_superuser']

class TeamAdmin(admin.ModelAdmin):
    inlines=[UserInline]

admin.site.unregister(Group)
# Register your models here.

admin.site.register(Team, TeamAdmin)
admin.site.register(User,UserAdmin)