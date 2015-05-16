from django.conf.urls import patterns, include, url
from django.contrib import admin
from insta import views
from insta.models import coffeeMaker
    
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'instacoffee.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^presence/$', views.presence, name='presence'),
    url(r'^startTime/$', views.startTime, name='startTime'),
    url(r'^shutdownTimer/$', views.shutdownTimer, name='shutdownTimer'),
    url(r'^backendLoop/', views.backendLoop, name='backendLoop'),
    url(r'^ready/$', views.ready, name='ready'),
)

# Set the defaults
device = coffeeMaker.objects.filter(name='Insta').get()
device.loopOn = "false"
device.powerButton = "off"
device.startTimeButton = "off"
device.startTime = "12:00"
device.shutdownTimer = "01:00"
device.turnOffTime = ""
device.tweet = "off"
device.coffie = "off"
device.pictureTaken = "off"
device.panPresence = "false"
device.coffeeReady = "false"
device.readyTime = ""
device.consumer_key = "eO96ZowsEhEdmvpioGNBrQxzE" 
device.consumer_secret = "nKPGmuSAVdK9UQV2h1jFcQ0fec4OLOlaDkTWdu8tbVkkKzZYWj"
device.access_token = "1428460136-TSXqHkUqEzaepLpU7orUIwA6lZfyfRmLuurvUDB"
device.access_token_secret = "r7nk7u1yaFfsSZl8QdABHv9N7KpAi99qZOofVFBvz0CB0"
device.save()