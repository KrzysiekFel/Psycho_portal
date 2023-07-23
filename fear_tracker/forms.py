from django import forms
from .models import FearTracker
from .widget import DatePickerInput, TimePickerInput
from typing import List, Type, Dict


class FearTrackerForm(forms.ModelForm):
    class Meta:
        model: Type[FearTracker] = FearTracker
        fields: List[str] = ['date', 'fear_level', 'time', 'activity', 'disturbing_thoughts']
        widgets: Dict[str, forms.widgets.Widget] = {
            'date': DatePickerInput(),
            'time': TimePickerInput(),
        }
