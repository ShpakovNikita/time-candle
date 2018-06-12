from django import forms
from time_candle.enums.status import status_dict, Status
from time_candle.enums.priority import priority_dict, Priority


class ChangeProfileForm(forms.Form):
    nickname = forms.CharField(max_length=30,
                               required=True)
    about = forms.CharField(max_length=550, required=False)
