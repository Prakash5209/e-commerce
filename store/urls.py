from django.urls import path

from store.views import HomeTemplateView


app_name = 'store'

urlpatterns = [
    path('',HomeTemplateView.as_view(),name='store'),
]
