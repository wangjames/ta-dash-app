from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^$', views.list_view, name='index'),
    url('^', include('django.contrib.auth.urls')),
    url('^register/$', views.register, name='register'),
]