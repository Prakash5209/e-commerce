from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

from store.models import CarouselImage


User = get_user_model()

class HomeTemplateView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['user'] = get_user_model()
        context['CarouselImage'] = CarouselImage.objects.all()
        return context
