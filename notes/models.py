from django.db import models
from django.contrib.auth.models import User
    
class Notes(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes") 
    title = models.CharField(max_length=50)
    description = models.TextField()

    def getAllNotes(self):
        return self.notes.all()
       
class Pengguna(User):
    class Meta:
        proxy = True
    
    def getAllNotesUser(self):
        return list(self.notes.all())

    def getNotes(self, notesId):
        try:
            return self.notes.filter(id=notesId).get()
        except:
            return None
    
    def deleteNotes(self, notesId):
        notes = self.notes.filter(id=notesId).delete()
        return notes
    
    def createNotes(self, notesTitle):
        notes = Notes.objects.create(name=notesTitle, owner=self)
        notes.save()
        return notes