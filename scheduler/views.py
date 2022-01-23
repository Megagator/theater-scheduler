from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Theater, Movie


def index(request):
    return render(request, "scheduler/index.html")

def create_event(request):
    print(request.POST)
    return HttpResponseRedirect(reverse('scheduler:index'))

def theaters(request):
    theaters = get_list_or_404(Theater.objects.order_by('short_name'))
    ctx = { 'theaters': theaters }

    return render(request, "scheduler/theaters.html", ctx)

def theater_schedule(request, theater_short_name):
    theater = get_object_or_404(Theater, short_name=theater_short_name)
    ctx = {
        'theater': theater
    }
    return render(request, "scheduler/theater.html", ctx)

def movies(request):
    movies = get_list_or_404(Movie.objects.order_by('slug'))
    ctx = { 'movies': movies }

    return render(request, "scheduler/movies.html", ctx)

def movie_schedule(request, movie_name):
    movie = get_object_or_404(Movie, slug=movie_name)
    ctx = { 'movie': movie }
    return render(request, "scheduler/movie.html", ctx)

