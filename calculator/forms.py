from django import forms


class ElementMatrix(forms.Form):
    element = forms.FloatField()


class CalculatorForm(forms.Form):
    size = forms.IntegerField()
    matrix = forms.formset_factory(forms.formset_factory(ElementMatrix, extra=size), extra=size)
    vector = forms.formset_factory(ElementMatrix, extra=size)
    e = forms.FloatField()
