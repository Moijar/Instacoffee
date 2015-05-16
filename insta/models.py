from django.db import models

# Create your models here.
class coffeeMaker(models.Model):
    name = models.CharField(max_length=200, blank=True, default='Insta')
    loopOn = models.CharField(max_length=200, blank=True, default='false')
    powerButton = models.CharField(max_length=200, blank=True, default='off')
    startTimeButton = models.CharField(max_length=200, blank=True, default='off')
    startTime = models.CharField(max_length=200, blank=True, default='12:00')
    shutdownTimer = models.CharField(max_length=200, blank=True, default='01:00')
    turnOffTime = models.CharField(max_length=200, blank=True, default='')
    tweet = models.CharField(max_length=200, blank=True, default='off')
    coffie = models.CharField(max_length=200, blank=True, default='off')
    pictureTaken = models.CharField(max_length=200, blank=True, default='false')
    panPresence = models.CharField(max_length=200, blank=True, default='false')
    coffeeReady = models.CharField(max_length=200, blank=True, default='false')
    readyTime = models.CharField(max_length=200, blank=True, default='')
    consumer_key = models.CharField(max_length=200, blank=True, default='eO96ZowsEhEdmvpioGNBrQxzE')
    consumer_secret = models.CharField(max_length=200, blank=True, default='"nKPGmuSAVdK9UQV2h1jFcQ0fec4OLOlaDkTWdu8tbVkkKzZYWj",')
    access_token = models.CharField(max_length=200, blank=True, default='1428460136-TSXqHkUqEzaepLpU7orUIwA6lZfyfRmLuurvUDB')
    access_token_secret = models.CharField(max_length=200, blank=True, default='r7nk7u1yaFfsSZl8QdABHv9N7KpAi99qZOofVFBvz0CB0')
    
    