from django.shortcuts import render, redirect,reverse 
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView , ListView , DetailView, CreateView, UpdateView , DeleteView
from .models import Lead 
from .forms import LeadModelForm,CustomUserCreationForm


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
    queryset = Lead.objects.all()
    context_object_name = "leads"


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


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead":lead
    }
    return render(request,'leads/lead_detail.html',context=context)

class LeadCreateView(LoginRequiredMixin,CreateView):
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

class LeadUpdateView(LoginRequiredMixin,UpdateView):
    template_name = 'leads/lead_update.html'
    queryset = Lead.objects.all() 
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")


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

class LeadDeleteView(LoginRequiredMixin,DeleteView):
    template_name = 'leads/lead_delete.html'
    queryset = Lead.objects.all() 

    def get_success_url(self):
        return reverse("leads:lead-list")

def lead_delete(request,pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")