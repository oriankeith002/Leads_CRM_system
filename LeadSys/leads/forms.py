from django import forms 
from django.contrib.auth.forms import UserCreationForm,UsernameField
from django.contrib.auth import get_user_model
from .models import Lead,Agent

User = get_user_model()

# CHOICES  = (
#     ('Agent 1','Agent 1'),
#     ('Agent 2','Agent 2'),
#     ('Agent 3','Agent 3')
# )
class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('first_name','last_name','age','agent')

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ("username",)
        field_classes = {'username':UsernameField}


class AssignAgentForm(forms.Form):
    # agent = forms.ChoiceField(choices=CHOICES)
    agent  = forms.ModelChoiceField(queryset=Agent.objects.none())

    # overiding the init method
    def __init__(self, *args, **kwargs):
        # accessing kwargs from view
        # print(kwargs)
        request = kwargs.pop("request") # removing since django forms don't expect request keyword
        # print(request.user) # this user is an organisor
        
        # now we get the queryset we want to  use to populate in the above user
        agents = Agent.objects.filter(organisation=request.user.userprofile)

        # now calling the __init__ method with original expected keyword arguments.
        super(AssignAgentForm,self).__init__(*args, **kwargs) 
        
        # updating the already defined queryset
        self.fields["agents"].queryset = agents  

        