from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('whoami', TemplateView.as_view(template_name='whoami.html'), name='whoami'),
]