from django.shortcuts import render, reverse 
from django.views.generic import ListView,CreateView,DetailView,DeleteView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin 
import random
# Create your views here.

class AgentListView(OrganisorAndLoginRequiredMixin,ListView):
    template_name = "agents/agent_list.html"

    # alternative to queryset
    def get_queryset(self): 
        organisation = self.request.user.userprofile # getting userprofile model of the logged in user
        return Agent.objects.filter(organisation=organisation)
    

class AgentCreateView(OrganisorAndLoginRequiredMixin,CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm 

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        # now using an actual user account 
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{random.randint(0,1000000)}") # assigning a random password to user
        user.save()
        # create agent object
        Agent.objects.create(
            user = user,
            organisation = self.request.user.userprofile
        )
        
        # sending an email to created user
        send_mail(
            subject = "You are invited to be an agent on LeadSys",
            message = "You were initiated as an agent on LeadSys CRM. Please Login to work",
            from_email = "admin@leadsys.com",
            recipient_list = [user.email]
        )

        # agent = form.save(commit=False) # saving form object without commiting it to db
        # # getting organisation from user profile
        # agent.organisation = self.request.user.userprofile
        # # saving the agent object to db
        # agent.save()
        return super(AgentCreateView,self).form_valid(form)
    

class AgentDetailView(OrganisorAndLoginRequiredMixin,DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self): 
        organisation = self.request.user.userprofile 
        return Agent.objects.filter(organisation=organisation)
    
    

class AgentUpdateView(OrganisorAndLoginRequiredMixin,UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm 

    def get_queryset(self):
        organisation = self.request.user.userprofile 
        return Agent.objects.filter(organisation=organisation)
    
    def get_success_url(self):
        return reverse("agents:agent-list")


class AgentDeleteView(OrganisorAndLoginRequiredMixin,DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agents"

    def get_queryset(self):
        organisation = self.request.user.userprofile 
        return Agent.objects.filter(organisation=organisation) 
    
    def get_success_url(self):
        return reverse("agents:agent-list")
