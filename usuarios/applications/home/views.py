import datetime

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class FechaMixin(object):
    
    def get_context_data(self, **kwargs):
        context = super(FechaMixin, self).get_context_data(**kwargs)
        context["fecha"] = datetime.datetime.now()
        return context
    

class Index(LoginRequiredMixin,FechaMixin, TemplateView):
    template_name = 'home/page_index.html'
    login_url = reverse_lazy('user_app:login')



class PruebaFecha(FechaMixin, TemplateView):
    template_name = 'home/mixin.html'



