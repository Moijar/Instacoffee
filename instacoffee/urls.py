from django.conf.urls import patterns, include, url
from django.contrib import admin
from insta import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'instacoffee.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),

    url(r'^hello/', 'insta.views.hello'),
    url(r'^home/', 'insta.views.home'),
    url(r'^on/', 'insta.views.turnon'),
    url(r'^ajaxexample$', 'insta.views.main'),
    url(r'^ajaxexample_json$', 'insta.views.ajax')
)