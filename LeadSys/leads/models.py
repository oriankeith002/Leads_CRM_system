from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Custom User Model
class User(AbstractUser):
    pass


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
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE) # assigning a lead to an agent

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
      
# SIGNALS IN DJANGO
# creating a django signal that listens to the event when a user is created
# we want to automate the user profile creation when a new user is created in the database
# this function will handle the event once we get the signal 
# instance is the actual model that was save 
# created - whether model was created or not
def post_user_created_signal(sender,instance, created, **kwargs):
    print(instance)
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)







