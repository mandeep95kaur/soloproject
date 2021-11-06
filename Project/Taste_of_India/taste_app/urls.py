from django.urls import path
from .import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('home',views.home),
    path('users/<int:user_id>/edit',views.edit_user),
    path('users/update',views.update),
    path('reviews',views.review),
    path('add_review',views.create_review),
    path('reviews/<int:review_id>/like',views.like_review),
    path('reviews/<int:review_id>/unlike',views.unlike_review),
    path('reviews/<int:review_id>/delete',views.delete_review),
    path('logout', views.logout)
]