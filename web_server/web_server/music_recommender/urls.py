from django.views.generic import TemplateView
from django.conf.urls import url
from .views import get_recommendation

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'get_rec_bands', get_recommendation)
]