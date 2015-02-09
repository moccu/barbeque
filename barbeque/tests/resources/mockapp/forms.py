from django import forms


class MockForm(forms.Form):
    name = forms.CharField(max_length=255)
    headline = forms.CharField(max_length=255, required=False)
    subline = forms.CharField(max_length=255, required=False)
    text = forms.CharField(max_length=255)
