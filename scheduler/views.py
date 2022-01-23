from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse

import random, datetime

from .models import MovieViewingEvent, Theater, Movie


def index(request):
    days = {}
    day = datetime.date.today()
    days[day.__str__()] = 'Today'
    for _ in range(5):
        day += datetime.timedelta(days=1)
        days[day.__str__()] = day.strftime('%A, %b %-d')

    minutes = []
    for m in range(0, 60, 15):
        minutes.append('{:02d}'.format(m))

    events = MovieViewingEvent.objects.order_by('begins_at')
    movies = Movie.objects.order_by('slug')
    theaters = Theater.objects.order_by('short_name')
    ctx = {
        'events': events,
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

    return render(request, "scheduler/index.html", ctx)

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

    return HttpResponseRedirect(reverse('scheduler:index'))

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

