from django import forms

from employee.models import EmployeeModel

from datetime import datetime
from django.utils.timezone import make_aware
from django.forms import TextInput, MultiWidget, DateTimeField


class MinimalSplitDateTimeMultiWidget(MultiWidget):

    def __init__(self, widgets=None, attrs=None):
        if widgets is None:
            if attrs is None:
                attrs = {}
            date_attrs = attrs.copy()

            date_attrs['type'] = 'date'

            widgets = [
                TextInput(attrs=date_attrs)
            ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value, value.strftime('%H:%M')]
        return [None, None]

    def value_from_datadict(self, data, files, name):
        date_str = super().value_from_datadict(data, files, name)[0]

        if date_str == '':
            return None

        my_datetime = datetime.strptime(date_str, "%Y-%m-%d")

        return make_aware(my_datetime)


class EmployeeForm(forms.ModelForm):

    birth = DateTimeField(widget=MinimalSplitDateTimeMultiWidget())

    class Meta:
        model = EmployeeModel

        fields = [
            'name',
            'birth',
            'address',
            'phone_number',

            'link_to_own_website',
            'linkedin',
            'github',
            'email',

            'level_of_english',
            'main_programming_language',
            'desired_salary',
            'type_of_job',

            'description_about_yourself',
            'education',
            'hard_skills',
            'work_experience',
            'soft_skills',

            'image',
            'additional_files'
        ]
