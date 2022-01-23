from django.urls import path

from . import views

app_name = 'scheduler'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_event, name='create_event'),
    path('theaters/', views.theaters, name="theaters"),
    path('theaters/<theater_short_name>/', views.theater_schedule, name="theater_schedule"),
    path('movies/', views.movies, name="movies"),
    path('movies/<slug:movie_name>/', views.movie_schedule, name="movie_schedule")
]