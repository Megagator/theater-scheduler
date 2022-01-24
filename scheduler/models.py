from django.db import models
from django.utils.timezone import now
from django.utils.text import slugify

from math import floor

class Theater(models.Model):
    name = models.CharField(max_length=64)
    short_name = models.CharField(max_length=8, unique=True)
    created_at = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return '{} – {}'.format(self.short_name, self.name)

class Movie(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=134, editable=False, unique=True)
    release_year = models.IntegerField()
    duration_seconds = models.IntegerField("duration in seconds")

    def save(self, *args, **kwargs):
        # note that the slug will change if the name is updated so existing URLs will break
        self.slug = slugify(self, allow_unicode=True)
        super().save(*args, **kwargs)

    def friendly_duration(self):
        hours = floor(self.duration_seconds / 3600)
        minutes = round((self.duration_seconds - (hours * 3600)) / 60)

        if hours > 0:
            return "{}h {}m".format(hours, minutes)
        else:
            return "{}m".format(minutes)

    def color_code(self):
        return (self.id % 10) + 1

    def __str__(self):
        return '{} ({})'.format(self.name, self.release_year)

class MovieViewingEvent(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    begins_at = models.DateTimeField()

    def __str__(self):
        return '{} in theater {} at {}'.format(self.movie, self.theater.short_name, self.begins_at.strftime("%H:%M on %m/%d"))
