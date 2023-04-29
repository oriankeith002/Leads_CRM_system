from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin 

class OrganisorAndLoginRequiredMixin(AccessMixin):
    """Verify that current user is authenticated and is an organisor. """

    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_authenticated or not request.user.is_organisor:
            return redirect("leads:lead-list")
        return super().dispatch(request,*args,**kwargs)
    
