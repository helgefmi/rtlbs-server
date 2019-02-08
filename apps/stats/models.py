# coding: utf-8
from django.db import models


class Run(models.Model):
    id = models.TextField(primary_key=True)
    link = models.TextField()
    category = models.ForeignKey('stats.Category', null=True, blank=True, on_delete=models.SET_NULL)
    comment = models.TextField(null=True, blank=True)
    status = models.TextField()
    time = models.IntegerField()
    player = models.ForeignKey('stats.Player', on_delete=models.CASCADE)
    moderator = models.ForeignKey('stats.Player', null=True, blank=True, on_delete=models.SET_NULL,
                                  related_name='moderated_run_set')
    date = models.DateField()
    emulated = models.BooleanField()


class Player(models.Model):
    id = models.TextField(primary_key=True)
    link = models.TextField()
    signed_up = models.DateTimeField()
    location = models.TextField()
    twitch_url = models.TextField(null=True, blank=True)


class Category(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    type = models.TextField()
