from django.db import models

from Auth.models import Auth
from Books.models import Book


class Comments(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_comment')
    content = models.TextField()
    user = models.ForeignKey(Auth, on_delete=models.CASCADE, related_name='user_comment')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content} on {self.book.title}"





    


