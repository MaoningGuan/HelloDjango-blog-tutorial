#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import path

from . import views
from .feeds import AllPostsRssFeed

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive'),
    path('category/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('tags/<int:pk>/', views.TagView.as_view(), name='tag'),

    # RSS链接，记得在顶部引入 AllPostsRssFeed
    path('all/rss/', AllPostsRssFeed(), name='rss'),
]
