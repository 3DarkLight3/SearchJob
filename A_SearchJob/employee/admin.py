from django.contrib import admin
from employee.models import EmployeeModel


class EmployeeAdmin(admin.ModelAdmin):

    list_display = ('name', 'birth', 'phone_number', 'level_of_english', 'main_programming_language', 'type_of_job')

    list_display_links = ('name', 'birth')
    list_editable = ('level_of_english', 'main_programming_language', 'type_of_job')
    list_filter = ('main_programming_language', 'level_of_english', 'type_of_job')
    search_fields = ('main_programming_language', 'type_of_job')


admin.site.register(EmployeeModel, EmployeeAdmin)
