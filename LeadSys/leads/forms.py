from django import forms 
from .models import Lead


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        field = ('first_name','last_name','age','agent')