from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

app_name = 'pages'
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^contact/$', views.contact, name="contact"),
    url(r'^thanks/$', TemplateView.as_view(template_name="pages/thanks.html"), name="thanks"),
]