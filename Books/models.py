from django.db import models

from Auth.models import Auth


class Book(models.Model):
    title= models.CharField(max_length=100)
    author= models.CharField(max_length=100)
    description= models.TextField()
    cover_image= models.ImageField(upload_to='static/books-images/', null=True, blank=True)
    published_by = models.ForeignKey(Auth, on_delete=models.CASCADE, related_name='published_books')
    created_at= models.DateField(auto_now_add=True)


    def __str__(self):
        return self.title +" by "+ self.author

     
