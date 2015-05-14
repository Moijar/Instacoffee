from django.conf.urls import patterns, include, url
from django.contrib import admin
from insta import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'instacoffee.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^presence/$', views.presence, name='presence'),
    url(r'^startTime/$', views.startTime, name='startTime'),
    url(r'^shutdownTimer/$', views.shutdownTimer, name='shutdownTimer'),
    url(r'^backendLoop/', views.backendLoop, name='backendLoop')
)