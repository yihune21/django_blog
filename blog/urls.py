# blog/urls.py
from django.urls import path
from . import views
from .feeds import LatestPostsFeed

urlpatterns = [
    
    path("", views.blog_index, name="blog_index"),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("category/<category>/", views.blog_category, name="blog_category"),
    path("search/" , views.blog_search, name = 'blog_search'),
    path("feed/", LatestPostsFeed(), name="blog_feed"),
]