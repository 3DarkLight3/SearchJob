from django import forms
from story.models import StoryModel


class StoryForm(forms.ModelForm):

    class Meta:
        model = StoryModel
        fields = [
            'headline',
            'title',
            'text',

            'for_who',
            'comments'
        ]
