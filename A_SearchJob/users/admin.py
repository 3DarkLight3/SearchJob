from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User_main = get_user_model()


@admin.register(User_main)
class UserAdmin(UserAdmin):
    list_display = ['first_name', 'last_name', 'id']
    list_editable = ['first_name', 'last_name']
    list_display_links = ['id']
