from django import forms


class DatePickerInput(forms.DateInput):
    input_type: str = 'date'


class TimePickerInput(forms.TimeInput):
    input_type: str = 'time'
