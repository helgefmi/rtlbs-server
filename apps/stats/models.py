# coding: utf-8
from django.db import models


class Run(models.Model):
    id = models.TextField(primary_key=True)
    link = models.TextField()
    category = models.ForeignKey('stats.Category', null=True, blank=True, on_delete=models.SET_NULL)
    comment = models.TextField(null=True, blank=True)
    status = models.TextField(db_index=True)
    time = models.IntegerField()
    player = models.ForeignKey('stats.Player', on_delete=models.CASCADE)
    moderator = models.ForeignKey('stats.Player', null=True, blank=True, on_delete=models.SET_NULL,
                                  related_name='moderated_run_set')
    date = models.DateField(db_index=True)
    emulated = models.NullBooleanField(blank=True)

    class Meta:
        ordering = ['date']


class Player(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    link = models.TextField(blank=True)
    signed_up = models.DateTimeField(null=True, blank=True)
    location = models.TextField(blank=True)
    twitch_url = models.TextField(null=True, blank=True)


class Category(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    type = models.TextField()
