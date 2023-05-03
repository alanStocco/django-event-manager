from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import MinValueValidator

class CustomUser(AbstractUser):
    def generate_tokens(self):
        refresh = RefreshToken.for_user(self)
        access = refresh.access_token
        return str(access), str(refresh) # TODO need cast to str?
    def __str__(self):
        return self.email
    
class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    attendees = models.ManyToManyField(CustomUser, related_name='events_attending', blank=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='events_owned')
    max_capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.name