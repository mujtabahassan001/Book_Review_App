from django.urls import path

from .views import ReviewsListCreateView, ReviewsRetrieveUpdateDestroyView


urlpatterns = [
    path('books/reviews/', ReviewsListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewsRetrieveUpdateDestroyView.as_view(), name='review-detail-update-delete'),
]