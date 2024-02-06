from django import forms
from employer.models import EmployerModel


class EmployerForm(forms.ModelForm):

    class Meta:
        model = EmployerModel

        fields = [
            'name_of_job',
            'name_of_company',
            'location',

            'required_english',
            'type_of_job',
            'main_programming_language',

            'lower_salary',
            'higher_salary',

            'remote_job',
            'min_experience',

            'benefits_of_job',
            'responsibilities_of_job',
            'requirements_of_job',

            'time_work',
            'link_to_own_website',
            'linkedin',
            'email',
            'phone_number'
        ]
