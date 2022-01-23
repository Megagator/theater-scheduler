from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('theaters/', views.theaters, name="theaters"),
    path('theaters/<theater_short_name>/', views.theater_schedule, name="theater_schedule"),
    path('movies/', views.movies, name="movies"),
    path('movies/<slug:movie_name>/', views.movie_schedule, name="movie_schedule")
]