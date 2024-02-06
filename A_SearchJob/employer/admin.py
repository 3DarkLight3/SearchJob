from django.contrib import admin
from employer.models import EmployerModel


class EmployerAdmin(admin.ModelAdmin):

    list_display = ('name_of_company', 'name_of_job', 'location', 'remote_job')

    list_display_links = ('name_of_company', )
    list_editable = ('location', 'remote_job')
    list_filter = ('type_of_job', 'required_english', 'main_programming_language', 'lower_salary',
                   'higher_salary', 'remote_job', 'min_experience')
    search_fields = ('location', 'name_of_job', 'name_of_company', 'type_of_job', 'main_programming_language')


admin.site.register(EmployerModel, EmployerAdmin)
