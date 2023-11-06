from django import forms

class TransportationForm(forms.Form):
    supply = forms.CharField(label='Supply', required=True)
    demand = forms.CharField(label='Demand', required=True)
    cost_matrix = forms.CharField(label='Cost Matrix', widget=forms.Textarea(attrs={'rows': 6, 'cols': 30, 'placeholder': '## space is mandatory in between two element ##\ne.g.\n1 2 3\n4 5 6\n7 8 9 '}), required=True)


