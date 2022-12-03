from django.db import models

class chek(models.Model):
    date = models.DateTimeField(auto_now_add=False, blank=True, null=True)