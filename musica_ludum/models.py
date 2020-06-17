from django.db import models
from django.contrib.auth.models import User

class Composition(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="composer")
    piece_name = models.CharField(max_length=100)
    mrnn_name = models.CharField(max_length=100, null=True)
    prnn_name = models.CharField(max_length=100, null=True)

class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="friendship_creator_set")
    friend = models.ForeignKey(User, on_delete=models.PROTECT, related_name="friend_set")

class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="score_of_user")
    song = models.CharField(max_length=100)