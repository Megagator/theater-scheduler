from django.db import models
from django.forms import DurationField
from django.utils.timezone import now
from django.utils.text import slugify

from math import floor
from datetime import timedelta

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

def get_movie_viewing_events_on(date, all_theaters=None):
    if not all_theaters:
        all_theaters = Theater.objects.order_by('short_name')

    # empty set of theaters to account for theaters with no events
    events_by_theater = {}
    for theater in all_theaters:
        events_by_theater[(theater.id, theater.short_name)] = []

    events = MovieViewingEvent.objects.order_by('begins_at').filter(begins_at__year=date.year,
        begins_at__month=date.month,
        begins_at__day=date.day
    )

    for event in events:
        events_by_theater[(event.theater.id, event.theater.short_name)].append(event)

    return events_by_theater


def get_least_busy_available_theater(new_event_begins_at, movie_id):
    events_by_theater = get_movie_viewing_events_on(new_event_begins_at)
    events_by_least_busy = dict(sorted(events_by_theater.items(), key=lambda v: len(v[1])))

    movie = Movie.objects.get(pk=movie_id)
    duration_seconds = movie.duration_seconds

    new_event_ends_at = new_event_begins_at + timedelta(seconds=duration_seconds)
    for theater, events in events_by_least_busy.items():
        # short circuit if there are no events to conflict with
        if len(events) == 0:
            return theater[0]

        for event in events:
            event_ends_at = event.begins_at + timedelta(seconds=event.movie.duration_seconds)

            # if the next event in this theater starts after the proposed ends, we're clear
            if event.begins_at > new_event_ends_at:
                return theater[0]

            # if the next event in this theater ends before the proposed begins, we must
            # keep searching for conflicting events
            if event_ends_at < new_event_begins_at:
                continue

            # otherwise, we must have a conflict here, so try the next theater
            break

    # we have exhasuted the theaters, so there is no availability
    return None
