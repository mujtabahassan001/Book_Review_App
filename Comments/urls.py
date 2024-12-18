from django.urls import path

from .views import CommentListCreateView, CommentRetrieveUpdateDestroyView


urlpatterns = [
    path('books/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment-detail-update-delete'),
]