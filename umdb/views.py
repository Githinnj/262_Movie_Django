from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser,Movie
from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {'user': request.user})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'register.html', {'error_message': 'Passwords do not match'})

        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error_message': 'Username already exists'})

        user = CustomUser.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        user.save()
        return redirect('login')
    return render(request, 'register.html')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    return render(request, 'login.html')

def custom_logout(request):
    logout(request)
    return redirect('home')


def movie_registration(request):
    if request.method == 'POST':
        # Retrieve form data
        title = request.POST.get('title')
        poster = request.FILES.get('poster')
        description = request.POST.get('description')
        release_date = request.POST.get('release_date')
        actors = request.POST.get('actors')
        genre = request.POST.get('genre')
        trailer_link = request.POST.get('trailer_link')
                # Get the logged-in user
        user = request.user
        # Create and save movie object
        movie = Movie.objects.create(
            title=title,
            poster=poster,
            description=description,
            release_date=release_date,
            actors=actors,
            genre=genre,
            trailer_link=trailer_link,
            user=user
        )
        movie.save()
        return redirect('home')  # Redirect to home page after movie registration
    
    return render(request, 'movie_registration.html')

from django.shortcuts import render, redirect
from .models import Movie

def movie_details(request):
    if request.user.is_authenticated:
        # Retrieve genre filter from query string
        genre_filter = request.GET.get('genre', None)
        search_query = request.GET.get('search', None)
        
        if genre_filter:
            # If a genre is selected, filter movies by genre
            movies = Movie.objects.filter(genre=genre_filter)
        else:
            # If no genre is selected, retrieve all movies
            movies = Movie.objects.all()
        
        if search_query:
            # If a search query is provided, filter movies by title containing the search query
            movies = movies.filter(title__icontains=search_query)
        
        # Retrieve distinct genres from the movies
        genres = Movie.objects.values_list('genre', flat=True).distinct()
        
        return render(request, 'movie_details.html', {'movies': movies, 'genres': genres, 'selected_genre': genre_filter})
    else:
        # Redirect to login page if the user is not authenticated
        return redirect('login')

def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.user.is_authenticated and movie.user == request.user:
        if request.method == 'POST':
            # Update movie details
            movie.title = request.POST.get('title')
            movie.description = request.POST.get('description')
            movie.release_date = request.POST.get('release_date')
            movie.actors = request.POST.get('actors')
            movie.genre = request.POST.get('genre')
            movie.trailer_link = request.POST.get('trailer_link')
            if 'poster' in request.FILES:
                movie.poster = request.FILES['poster']
            movie.save()
            return redirect('movie_details')
        else:
            return render(request, 'edit_movie.html', {'movie': movie})
    else:
        # Redirect to movie details page if the user is not the owner of the movie
        return redirect('movie_details')
    

def delete_movie(request, movie_id):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, id=movie_id)
        if movie.user == request.user:  # Ensure that only the owner of the movie can delete it
            movie.delete()
        return redirect('movie_details')
    else:
        return redirect('login')
    

from django.contrib.auth import update_session_auth_hash

def edit_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Get the updated user details from the POST data
            new_username = request.POST.get('username')
            new_first_name = request.POST.get('first_name')
            new_last_name = request.POST.get('last_name')
            new_email = request.POST.get('email')

            # Update the user object with the new details
            user = request.user
            user.username = new_username
            user.first_name = new_first_name
            user.last_name = new_last_name
            user.email = new_email
            user.save()

            update_session_auth_hash(request, user)  # To update the session with the new user details
            return redirect('home')  # Redirect to the profile page after successful edit
        else:
            return render(request, 'edit_user.html', {'user': request.user})
    else:
        return redirect('login')
    

from .models import Movie, ReviewRating
from django.contrib.auth.decorators import login_required

@login_required
def rate_review_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        text = request.POST.get('text')
        if rating:
            rating_obj = ReviewRating.objects.create(movie=movie, user=request.user, rating=rating, text=text)
            rating_obj.save()
            return redirect('movie_details')  # Redirect to movie details page or any other page
        else:
            # Handle error if rating is not provided
            return render(request, 'movie_review.html', {'error_message': 'Please select a rating'})
    return render(request, 'movie_review.html', {'movie': movie})

@login_required
def all_movies(request,movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = ReviewRating.objects.filter(movie=movie)
    if request.user.is_authenticated:
        return render(request, 'all_movie_details.html', {'movies': movie,'reviews': reviews})
    else:
        return redirect('login')