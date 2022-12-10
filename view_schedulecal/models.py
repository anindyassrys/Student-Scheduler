from django.db import models
from django.contrib.auth.models import User

class ScheduleCalendar(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateTimeField()
    detail = models.TextField()
    owner = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title