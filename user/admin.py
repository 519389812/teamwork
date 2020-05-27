from django.contrib import admin
from user.models import User
from django.contrib.auth.admin import UserAdmin


admin.site.register(User, UserAdmin)

admin.site.site_header = 'Teamwork管理系统'
admin.site.site_title = 'Teamwork管理系统'
admin.site.index_title = 'Teamwork管理系统'
