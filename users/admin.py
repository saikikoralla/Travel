from django.contrib import admin
from .models import Profile,User
from django.contrib.auth import get_user_model
#from django.contrib.auth.admin import UserAdmin
User=get_user_model()
# Register your models here.
"""
class UserModelAdmin(UserAdmin):
    # Customising the view of admin panel, which fields to be shown
    list_display = ('id', 'email', 'is_superuser')
    # Helps to filter out data at admin panel
    list_filter = ('is_superuser',)
    # Categorised the data according to our need.
    fieldsets = [
        ('User Credentials', {'fields': ['email', 'password']}),
        ('Roles', {'fields': ['is_superuser']}),
    ]

    add_fieldsets = [
        (
            None,
            {'fields': ('email','password', 'confirm_password')}
        )
    ]

    search_fields = ['email']
    ordering = ['email']
"""

admin.site.register(User)
admin.site.register(Profile)
