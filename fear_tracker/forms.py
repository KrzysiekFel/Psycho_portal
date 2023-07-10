from django import forms
from .models import FearTracker
from .widget import DatePickerInput, TimePickerInput


class FearTrackerForm(forms.ModelForm):
    class Meta:
        model = FearTracker
        fields = ['date', 'fear_level', 'time', 'activity', 'disturbing_thoughts']
        widgets = {
            'date': DatePickerInput(),
            'time': TimePickerInput(),
        }
