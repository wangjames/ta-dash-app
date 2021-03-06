from django.conf.urls import url, include

from ta_dash import views
from django.contrib.auth import views as authviews

urlpatterns = [
    url(r'^$', views.main, name='main' ),
    url(r'^index/$', views.list_view, name='index'),
    url(r'^class/(?P<class_index>[0-9]+)/$', views.class_index, name= 'class_index'),
    url(r'^class/(?P<class_index>[0-9]+)/(?P<user_index>[0-9]+)/view_class_user/$', views.view_submissions_by_user, name="view_class_user"),
    url(r'^class/(?P<class_index>[0-9]+)/(?P<assignment_index>[0-9]+)/', views.view_assignment, name="assignment_index"),
    url(r'^class/(?P<class_index>[0-9]+)/invite/$', views.invite_user, name="invite_user"),
    url(r'^invites/(?P<class_index>[0-9]+)/$', views.accept_invite, name="accept_invite"),
    url(r'^invites/$', views.get_invites, name="invites"),
    url(r'^class/(?P<class_index>[0-9]+)/create_meeting/$', views.create_meeting, name="create_meeting"),
    url(r'^class/(?P<class_index>[0-9]+)/view_attendees/$', views.view_attendees, name="view_attendees"),
    url(r'^getsuggest/$', views.return_suggestions, name="get_suggest"),
    url(r'^login/$', authviews.login, name='login'),
    url('^', include('django.contrib.auth.urls')),
    url('^register/$', views.register, name='register'),
    url('^create/$', views.create_class, name="create_class"),
    url('^create/(?P<class_index>[0-9]+)', views.create_assignment, name="create_assignment"),
    url('^sign_s3', views.sign_s3, name="sign_s3")
]

