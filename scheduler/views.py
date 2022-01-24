from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse

import random, datetime

from .models import MovieViewingEvent, Theater, Movie

def schedule(request, date=None):
    days = {}
    day = datetime.date.today()
    days[str(day)] = 'Today'
    for _ in range(5):
        day += datetime.timedelta(days=1)
        days[str(day)] = day.strftime('%A, %b %-d')

    minutes = [0, 15, 30, 45]

    if type(date) == str:
        date_format = '%Y-%m-%d'
        date = datetime.datetime.strptime(date, date_format).date()
    else:
        date = datetime.date.today()

    events = MovieViewingEvent.objects.order_by('begins_at').filter(begins_at__year=date.year,
        begins_at__month=date.month,
        begins_at__day=date.day
    )
    # group by theater, sorted by short name
    events_by_theater = {}
    for event in events:
        if (event.theater.short_name not in events_by_theater):
            events_by_theater[event.theater.short_name] = []
        events_by_theater[event.theater.short_name].append(event)
    events_by_theater = dict(sorted(events_by_theater.items()))

    movies = Movie.objects.order_by('slug')
    theaters = Theater.objects.order_by('short_name')
    ctx = {
        'date_string': date.strftime('%A, %b. %-d'),
        'date_prev': str(date - datetime.timedelta(days=1)),
        'date_next': str(date + datetime.timedelta(days=1)),
        'events': events_by_theater,
        'movies': movies,
        'theaters': theaters,
        'random_movie': random.choice(movies).id,
        'random_theater': random.choice(theaters).id,
        'days': days,
        'hours': range(24),
        'minutes': minutes,
        'random_day': random.randint(0, len(days)),
        'random_hour': random.randint(0, 23),
        'random_minute': random.choice(minutes)
    }

    return render(request, "scheduler/schedule.html", ctx)

def create_event(request):
    try:
        time = ('{} {}:{}'.format(request.POST['event_day'], request.POST['event_hour'], request.POST['event_minute']))
        date_format = '%Y-%m-%d %H:%M'
        begins_at = datetime.datetime.strptime(time, date_format)

        new_event = MovieViewingEvent(
            movie_id = request.POST['movie_id'],
            theater_id = request.POST['theater_id'],
            begins_at = begins_at
        )
        new_event.save()
    except Exception as e:
        print(e)

    return HttpResponseRedirect(reverse('scheduler:future_schedule', args=(str(begins_at.date()),)))

def theaters(request):
    theaters = get_list_or_404(Theater.objects.order_by('short_name'))
    ctx = { 'theaters': theaters }

    return render(request, "scheduler/theaters.html", ctx)

def theater_schedule(request, theater_short_name):
    theater = get_object_or_404(Theater, short_name=theater_short_name)
    ctx = { 'theater': theater }
    return render(request, "scheduler/theater.html", ctx)

def movies(request):
    movies = get_list_or_404(Movie.objects.order_by('slug'))
    ctx = { 'movies': movies }

    return render(request, "scheduler/movies.html", ctx)

def movie_schedule(request, movie_name):
    movie = get_object_or_404(Movie, slug=movie_name)
    ctx = { 'movie': movie }
    return render(request, "scheduler/movie.html", ctx)

