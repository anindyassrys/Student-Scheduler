from django.db import models
from django.contrib.auth.models import User
    
class Notes(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes") 
    title = models.CharField(max_length=50)
    description = models.TextField()

    def getAllNotes(self):
        return self.notes.all()