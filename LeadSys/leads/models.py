from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Custom User Model
class User(AbstractUser):
    # these boolean fields will help with managing permissions of the user
    # specifying type of user whether organiser or agent
    is_organisor = models.BooleanField(default=True) # owns the entire organization
    # if you create an account you are by default the organisor of that account
    is_agent = models.BooleanField(default=False)
    

# create a user profile model that is linked to a user
# then link each agent to the parent user profile.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Every agent has one user
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email 

class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    agent = models.ForeignKey(Agent, null=True, blanK=True, on_delete=models.SET_NULL) # assigning a lead to an agent

    #  since every lead is associated with an agent
    # we need to track which organisation the agent falls under
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # this allows us to filter by the organization

    # every lead will be assigned to a category
    category = models.ForeignKey("Category", related_name="leads", null=True, blank=True, on_delete=models.SET_NULL) 


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
      
# SIGNALS IN DJANGO
# creating a django signal that listens to the event when a user is created
# we want to automate the user profile creation when a new user is created in the database
# this function will handle the event once we get the signal 
# instance is the actual model that was save 
# created - whether model was created or not
def post_user_created_signal(sender,instance, created, **kwargs):
    #print(instance)
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)



class Category(models.Model):
    # OUR 4 categories include : New , Contacted , Converted, Unconverted 
    name = models.CharField(max_length=30)
    organisation = models.ForeignKey(UserProfile,on_delete=models.CASCADE) # Tricky if you don't want to delete database choose ignore now when migrating.


    def __str__(self):
        return self.name


