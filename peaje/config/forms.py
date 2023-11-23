from django import forms

class CasillasFilterForm(forms.Form):
    num_casilla  = forms.IntegerField()