from django.shortcuts import render, reverse 
from django.views.generic import ListView,CreateView,DetailView,DeleteView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm
# Create your views here.

class AgentListView(LoginRequiredMixin,ListView):
    template_name = "agents/agent_list.html"

    # alternative to queryset
    def get_queryset(self): 
        return Agent.objects.all() 
    

class AgentCreateView(LoginRequiredMixin,CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm 

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        agent = form.save(commit=False) # saving form object without commiting it to db
        # getting organisation from user profile
        agent.organisation = self.request.user.userprofile
        # saving the agent object to db
        agent.save()
        return super(AgentCreateView,self).form_valid(form)
    

class AgentDetailView(LoginRequiredMixin,DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agents"

    def get_queryset(self): 
        return Agent.objects.all() 
    

class AgentUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm 

    def get_queryset(self):
        return Agent.objects.all()
    
    def get_success_url(self):
        return reverse("agents:agent-list")


class AgentDeleteView(LoginRequiredMixin,DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agents"

    def get_queryset(self): 
        return Agent.objects.all() 
    
    def get_success_url(self):
        return reverse("agents:agent-list")
