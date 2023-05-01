from django.shortcuts import render, redirect,reverse 
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import  TemplateView , ListView , DetailView, CreateView, UpdateView , DeleteView, FormView
from .models import Lead 
from .forms import LeadModelForm,CustomUserCreationForm,AssignAgentForm
from agents.mixins import OrganisorAndLoginRequiredMixins

# Create your views here.

class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

class LandingPageView(TemplateView):
    template_name = "landing.html"


def landing_page(request):
    return render(request, "landing.html")


class LeadListView(LoginRequiredMixin,ListView):
    template_name = 'leads/lead_list.html'
    # WE want to filter the leads for a specific agent
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user # getting  logged in user

        # INITIAL QUERYSET FOR THE LEADS OF THE ENTIRE ORGANISATION

        # queryset = Lead.object.all() # we avoid getting all the leads across all organizatons
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile,agent__isnull=False)  
        else: # if they are not organisor then they are agent
        # if user.is_agent: # checking if logged in user is an agent
            # we want to filter the leads for the agent that is logged in based on their specific organisation
            queryset = Lead.objects.filter(agent__user=user.agent.organisation,agent__isnull=False) # this doesn't make extra queries on the database
            # Add agent__isnull=False to ensure querysets return only assigned leads.

            ## OBTAINED ALL LEADS OF THE ENTIRE ORGANISATION FOR either organisor or agent
            # filtering leads for the current logged in agent.
            # agent_user means filter the lead based on an agent where that agent has a user equal to the self.request.user
            queryset = queryset.filter(agent__user=user)
        return queryset # the final returned queryset


    # Handling unassigned leads. 
    # we overide the get_context_data method
    # grab existing context using the super command
    # then return the context

    def get_context_data(self,**kwargs):
        user = self.request.user
        # getting the existing context
        context = super(LeadListView,self).get_context_data(**kwargs)

        # only users who are organisors can update the context
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=True) 
            # filtering for where the agent is null with agent__isnull=True
            # we pass in a dictionary of context we want to pass in
            context.update({
                "unassigned_leads": queryset
            })

        return context

def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    return render(request,'leads/lead_list.html', context=context)

class LeadDetailView(LoginRequiredMixin,DetailView):
    template_name = 'leads/lead_detail.html'
    queryset = Lead.objects.all()
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(agent__user=user.agent.organisation) 
            queryset = queryset.filter(agent__user=user)
        return queryset 


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead":lead
    }
    return render(request,'leads/lead_detail.html',context=context)

class LeadCreateView(OrganisorAndLoginRequiredMixins,CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self,form):
        # TODO send email using django
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com "]
        )
        return super(LeadCreateView,self).form_valid(form) #continuing with the form 

def lead_create(request):
    form = LeadModelForm() # empty uninstantiated form 

    # Check if method is a POST request
    if request.method == "POST":
        form = LeadModelForm(request.POST)

        # checking if form is valid
        if form.is_valid():
            form.save()
            return redirect('/leads') # redirect us to leads page after filling form
        
    context = {
        "form": form
    }
    return render(request,'leads/lead_create.html',context=context)

class LeadUpdateView(OrganisorAndLoginRequiredMixins,UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)
     


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead) 
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        "form":form,
        "lead":lead
    }
    return render(request,"leads/lead_update.html",context=context)

class LeadDeleteView(OrganisorAndLoginRequiredMixins,DeleteView):
    template_name = 'leads/lead_delete.html'

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)
     

def lead_delete(request,pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")



class AssignAgentView(OrganisorAndLoginRequiredMixins,FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self,**kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request # passing in the request into the form
        })
        return kwargs
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    

    def form_valid(self,form):
        #print(form.data)
        # we want to access the value that was submitted since this is not a modelform.
        agent = form.cleaned_data["agent"]
        # getting lead from the primary key
        lead = Lead.objects.get(id=self.kwargs["pk"]) 
        lead.agent = agent
        lead.save()

        return super(AssignAgentView, self).form_valid(form)