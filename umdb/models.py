from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Movie(models.Model):
    title = models.CharField(max_length=100)
    poster = models.ImageField(upload_to='posters/')
    description = models.TextField()
    release_date = models.DateField()
    actors = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    trailer_link = models.CharField(max_length=200)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,default=1)
    
    def __str__(self):
        return self.title
    

class ReviewRating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    rating = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.movie.title}"