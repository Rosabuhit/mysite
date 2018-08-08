from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.news, name='news'),
    url(r'^contact/$', views.contactView, name='contact'),
    url(r'^thanks/$', views.contactView, name='thanks'),
]