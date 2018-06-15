from django import forms


class ProjectForm(forms.Form):
    title = forms.CharField(
        label='project\'s title', max_length=30, required=True)
    description = forms.CharField(label='description', required=False,
                                  widget=forms.Textarea)
