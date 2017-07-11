from django.conf.urls import url, include

from . import views
from django.contrib.auth import views as authviews

urlpatterns = [
    url(r'^$', views.main, name='main' ),
    url(r'^index/$', views.list_view, name='index'),
    url(r'^class/(?P<class_index>[0-9]+)/$', views.class_index, name= 'class_index'),
    url(r'^class/(?P<class_index>[0-9]+)/(?P<assignment_index>[0-9]+)/', views.view_assignment, name="assignment_index"),
    url('^', include('django.contrib.auth.urls')),
    url('^register/$', views.register, name='register'),
    url('^create/$', views.create_class, name="create_class"),
    url('^create/(?P<class_index>[0-9]+)', views.create_assignment, name="create_assignment"),
    url('^create/(?P<class_index>[0-9]+)/(?P<assignment_index>[0-9]+)/', views.create_submission, name="create_submission"),
]