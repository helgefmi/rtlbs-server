# coding: utf-8
import os
import re
import urllib.parse

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify

from autoslug import AutoSlugField


class Segment(models.Model):
    name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='name', unique=True)
    sort = models.PositiveIntegerField(unique=True)

    class Meta:
        ordering = ['sort']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        return super().save(*args, **kwargs)


class Room(models.Model):
    segment = models.ForeignKey('rooms.Segment', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    sort = models.PositiveIntegerField()

    class Meta:
        ordering = ['segment__sort', 'sort']
        unique_together = [
            ['segment', 'sort']
        ]


def media_file_name(instance, filename):
    if '.' not in filename:
        return 'roomtimes/'

    ext = filename.split('.')[-1]
    new_filename = '_'.join([
        instance.player.username,
        instance.room.slug,
    ]) + '.' + ext

    i = 1
    while os.path.exists(os.path.join(settings.MEDIA_ROOT, 'roomtimes', new_filename)):
        i += 1
        new_filename = '_'.join([
            instance.player.username,
            instance.room.slug,
            str(i),
        ]) + '.' + ext

    return os.path.join('roomtimes', new_filename)


class RoomTime(models.Model):
    class LTTPHackVersion(object):
        V7 = 7
        V8 = 8
        V9 = 9

        CHOICES = (
            (V7, 'V7'),
            (V8, 'V8'),
            (V9, 'V9'),
        )

    player = models.ForeignKey('players.Player', on_delete=models.CASCADE)
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE)
    frames = models.DecimalField(max_digits=6, decimal_places=2)
    lag = models.IntegerField()
    idle = models.IntegerField(null=True, blank=True)
    menues = models.PositiveIntegerField()
    lttphack_version = models.IntegerField(choices=LTTPHackVersion.CHOICES,
                                           default=LTTPHackVersion.V9)
    description = models.TextField(blank=True)
    media = models.FileField(upload_to=media_file_name, blank=True)
    twitch_url = models.TextField(blank=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['room', 'frames']

    def save(self, *args, **kwargs):
        matcher = re.compile('^(\s*<p>\s*(<br>)?\s*<\/p>\s*)+$')
        if matcher.match(self.description):
            self.description = ''
        super().save(*args, **kwargs)

    def get_media(self):
        if self.twitch_url:
            embed_url = None

            match = re.compile('clips.twitch.tv/([^/]+)').search(self.twitch_url)
            if match:
                embed_url = 'https://clips.twitch.tv/embed?clip={}&autoplay=false'.format(match.group(1))

            match = re.compile('twitch.tv/videos/(\d+)').search(self.twitch_url)
            if match:
                embed_url = 'https://player.twitch.tv/?autoplay=false&video=v{}'.format(match.group(1))

            return {
                'embed_url': embed_url,
                'url': self.twitch_url,
                'type': 'twitch',
            }

        if self.media:
            return {
                'url': urllib.parse.urljoin(settings.API_URL, self.media.url),
                'type': 'video' if self.media.name.endswith('.mp4') else 'image',
                'filename': os.path.basename(self.media.name),
                'size': self.media.size
            }

        return {}
