from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Auth.utils import JWTAuthentication 
from .models import Book
from .serializer import BookSerializer


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user:
            raise PermissionDenied("User not authenticated.")
        serializer.save(published_by=self.request.user)


class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Book.objects.get(pk=self.kwargs['pk'])
        except Book.DoesNotExist:
            return Response({"details": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        book = self.get_object()
        if book:
            comments = book.book_comment.all()
            comments_data = [{"book_id": comment.book.id, "content": comment.content} for comment in comments]

            reviews = book.book_reviews.all()
            reviews_data = [{"book_id": review.book.id, "review": review.review} for review in reviews]

            book_data = BookSerializer(book).data
            book_data['comments'] = comments_data
            book_data['reviews'] = reviews_data

            return Response(book_data, status=status.HTTP_200_OK)

        return Response({"details": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        book = self.get_object()
        if book.published_by != request.user:
            raise PermissionDenied("You do not have permission to edit this book.")
        
        serializer = self.get_serializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"details":serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        book = self.get_object()
        if not book:
            return Response({"details": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        if book.published_by != request.user:
            raise PermissionDenied("You do not have permission to delete this book.")
        
        try:
            book.delete()
            return Response({"details": "Book deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"details": "Something went wrong ", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)