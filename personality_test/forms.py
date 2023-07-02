from django import forms
from .models import PersonalityTest


class PersonalityForm(forms.ModelForm):
    class Meta:
        model = PersonalityTest
        fields = ['question_1', 'question_2', 'question_3', 'question_4', 'question_5', 'question_6', 'question_7']
        help_texts = {
            'question_1': '1. Are generally sociable    2. Are generally quiet',
            'question_2': '1. Are focused on the outer world    2. Are focused on their inner world',
            'question_3': '1. Get energy by spending time with others   2. Get energy by spending time alone',
            'question_4': '1. Talk a lot & start conversations  2. Mostly listen & wait for others to talk first',
            'question_5': '1. Speak first, then think   2. Think first, then speak',
            'question_6': '1. Are quick to take action  2. Are slow to take action',
            'question_7': '1. Have many friends & many interests    2. Have a few deep friendships & refined interests',
        }
