from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

class AppointmentRequestManager(models.Manager):
    def getSentAppointmentRequests(self, sender):
        return self.filter(sender=sender)

    def getReceivedAppointmentRequests(self, receiver):
        return self.filter(receiver=receiver)

    def getAcceptedAppointmentRequests(self, user):
        return self.filter(Q(isAccepted=True), Q(sender=user) | Q(receiver=user))


class AppointmentRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sentAppointment")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receivedAppointment")
    datetime = models.DateTimeField()
    description = models.TextField()
    isAccepted = models.BooleanField(default=False)

    objects = AppointmentRequestManager()
