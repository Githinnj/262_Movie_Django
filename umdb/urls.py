from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('', views.home, name='home'),
    path('movie_registration/', views.movie_registration, name='movie_registration'), 
    path('movie_details/', views.movie_details, name='movie_details'), 
    path('edit_movie/<int:movie_id>/', views.edit_movie, name='edit_movie'),
    path('delete_movie/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('rate_review_movie/<int:movie_id>/', views.rate_review_movie, name='rate_review_movie'),
    path('all_movies/<int:movie_id>/', views.all_movies, name='all_movies'),
    # Add your other URLs
]