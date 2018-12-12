from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=200)
    imageUrl = models.CharField(max_length=250)

    def __str__(self):
        return "%s [%s]" % (self.name, self.email)


class Sender(models.Model):
    name = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=200)
    imageUrl = models.CharField(max_length=250)

    def __str__(self):
        return "%s [%s]" % (self.name, self.email)


class Message(models.Model):
    sender = models.ForeignKey(
        'Sender',
        on_delete=models.CASCADE,
        related_name='sender')
    recipient = models.ForeignKey(
        'Sender',
        on_delete=models.CASCADE,
        related_name='recipient')
    message = models.CharField(max_length=200)
    visible = models.IntegerField(default=1)
    timestamp = models.DateTimeField('date created')

    def __str__(self):
        return "%s [From: %s]" % (self.message, self.sender.email)
