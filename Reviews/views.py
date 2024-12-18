from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from Auth.utils import JWTAuthentication
from Books.models import Book
from .models import Reviews
from .serializer import ReviewsSerializer


class ReviewsListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reviews.objects.all().order_by('id')

    def perform_create(self, serializer):
        book_id = self.request.data.get('book')
        review = self.request.data.get('review')

        if not book_id:
            raise PermissionDenied("Book is required.")
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            raise PermissionDenied("Book not found.")

        if book.published_by == self.request.user:
            raise PermissionDenied("You cannot review your own book.")

        serializer.save(user=self.request.user, book=book, review=review)

class ReviewsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ReviewsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reviews.objects.all()

    def perform_update(self, serializer):
        reviews = self.get_object()

        if reviews.user != self.request.user:
            raise PermissionDenied("You can only edit your own reviews.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own reviews.")
        instance.delete()
