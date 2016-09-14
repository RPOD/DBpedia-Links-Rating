from django import forms

RANGES = [
    ('-1', '-1'),
    ('0', '0'),
    ('1', '1'),
]


class CreateRatingForm(forms.Form):
    vote = forms.ChoiceField(widget=forms.RadioSelect, choices=RANGES)
