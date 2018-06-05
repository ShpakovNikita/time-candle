from django import forms
from time_candle.enums.status import status_dict, Status
from time_candle.enums.priority import priority_dict, Priority

STATUS_CHOICES = tuple(status_dict.items())
PRIORITY_CHOICES = tuple(priority_dict.items())


class AddTask(forms.Form):
    title = forms.CharField(label='task\'s title', max_length=30, required=True)
    comment = forms.CharField(label='comment', max_length=155, required=False)
    deadline_time = forms.CharField(
        label='deadline', required=False,
        help_text='Optional. Format: YYYY-MM-DD hh:mm:ss')
    priority = forms.ChoiceField(
        label='priority', choices=PRIORITY_CHOICES, initial=Priority.MEDIUM,
        required=False)
    status = forms.ChoiceField(
        label='status', choices=STATUS_CHOICES, initial=Status.IN_PROGRESS,
        required=False)
    period = forms.IntegerField(label='period in days', required=False)


class AddProject(forms.Form):
    title = forms.CharField(
        label='project\'s title', max_length=30, required=True)
    description = forms.CharField(label='description', required=False)
