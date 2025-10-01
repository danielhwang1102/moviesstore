from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='movies.index'),
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create/', views.create_review,
        name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='movies.delete_review'),
    path('review/<int:review_id>/like/', views.like_review, name='review.like'),
    path('petitions/', views.petitions_page, name='movies.petitions_page'),
    path('petition/create/', views.create_petition, name='movies.create_petition'),
    path('petition/<int:petition_id>/like/', views.like_petition, name='movies.like_petition'),
]