from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Petition
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count

# Create your views here.
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
        {'template_data': template_data})
def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie).annotate(num_likes=Count('likes')).order_by('-num_likes')
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html',
        {'template_data': template_data})
@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)
@require_POST
@login_required
def like_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user in review.likes.all():
        review.likes.remove(request.user)
        liked = False
    else:
        review.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'likes_count': review.likes.count()})

@login_required
def petitions_page(request):
    petitions = Petition.objects.select_related('movie', 'user').annotate(likes_count=Count('likes')).order_by('-likes_count')
    movies = Movie.objects.all()
    template_data = {
        'petitions': petitions,
        'title': 'All Petitions',
        'movies': movies
    }
    return render(request, 'movies/petitions.html', {'template_data': template_data})

@login_required
def create_petition(request):
    if request.method == 'POST':
        movie_name = request.POST.get('movie_name')
        if movie_name:
            movie, created = Movie.objects.get_or_create(
                name=movie_name,
                defaults={'price': 0, 'description': 'Petitioned movie', 'image': 'movie_images/default.jpg'}
            )
            Petition.objects.create(movie=movie, user=request.user)
    return redirect('movies.petitions_page')

@require_POST
@login_required
def like_petition(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)
    if request.user in petition.likes.all():
        petition.likes.remove(request.user)
        liked = False
    else:
        petition.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'likes_count': petition.likes.count()})