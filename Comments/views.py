from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from Auth.utils import JWTAuthentication
from .models import Comments, Book
from .serializer import CommentsSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
    
        return Comments.objects.all().order_by('id')

    def perform_create(self, serializer):
        book_id = self.request.data.get('book')
        content = self.request.data.get('content')

        if not book_id:
            raise PermissionDenied("Book is required.")

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            raise PermissionDenied("Book not found.")

        if book.published_by == self.request.user:
            raise PermissionDenied("You cannot comment on your own book.")

        serializer.save(user=self.request.user, book=book, content=content)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = CommentsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Comments.objects.all()

    def perform_update(self, serializer):

        comment = self.get_object()
        if comment.user != self.request.user:
            raise PermissionDenied("You can only edit your own comments.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own comments.")
        instance.delete()
