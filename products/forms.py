from django import forms

class ProductFilterForm(forms.Form):
    sensitive = forms.BooleanField(required=False)
    name = forms.CharField(required=False)
    description = forms.CharField(required=False)
    price_from = forms.DecimalField(required=False)
    price_to = forms.DecimalField(required=False)