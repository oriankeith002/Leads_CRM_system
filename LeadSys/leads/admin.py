from django.contrib import admin
from .models import User, Agent, Lead,UserProfile

# Register your models here.
admin.site.register(User)
admin.site.register(Agent)
admin.site.register(Lead)
admin.site.register(UserProfile)
