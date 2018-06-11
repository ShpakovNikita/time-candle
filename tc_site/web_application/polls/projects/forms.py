from django import forms
from time_candle.enums.status import status_dict, Status
from time_candle.enums.priority import priority_dict, Priority


class AddProject(forms.Form):
    title = forms.CharField(
        label='project\'s title', max_length=30, required=True)
    description = forms.CharField(label='description', required=False,
                                  widget=forms.Textarea)
