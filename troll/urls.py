from django.urls import path, include

import troll.views
from .views import (
	PostListView, 
	PostDetailView, 
	PostCreateView,
	PostUpdateView,
	PostDeleteView,
	UserPostListView

)




from . import views

urlpatterns = [
	path('', troll.views.home, name ='troll-home'),
	path('posts', PostListView.as_view(), name ='troll-postcol'),
	path('user/<str:username>', UserPostListView.as_view(), name ='user-posts'),
	path('post/<int:pk>/', PostDetailView.as_view(), name ='post-detail'),
	path('post/new/', PostCreateView.as_view(), name ='post-create'),
	path('post/<int:pk>/update/', PostUpdateView.as_view(), name ='post-update'),
	path('post/<int:pk>/delete/', PostDeleteView.as_view(), name ='post-delete'),



]







