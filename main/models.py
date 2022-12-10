from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=300)
    detail=models.TextField()

    def __str__(self):
        return self.title

class Answer(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    detail=models.TextField()

    def __str__(self):
        return self.detail




