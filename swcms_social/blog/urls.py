from django.urls import path
from blog.views import PostListView, PostDetailView


urlpatterns = [
    path('blog', PostListView.as_view(), name='list'),
    path('blog/<int:pk>', PostDetailView.as_view(), name='detail'),
]

