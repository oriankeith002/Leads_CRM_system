from django import forms 
from django.contrib.auth.forms import UserCreationForm,UsernameField
from django.contrib.auth import get_user_model
from .models import Lead

User = get_user_model()

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        field = ('first_name','last_name','age','agent')

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User 
        files = ("username")
        field_classes = {'username':UsernameField}
