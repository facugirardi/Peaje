from django import forms

class CasillasFilterForm(forms.Form):
    num_casilla  = forms.IntegerField()

class TarifasFilterForm(forms.Form):
    num_tarifa  = forms.IntegerField()