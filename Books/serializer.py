from rest_framework import serializers

from Auth.serializer import LoginSerializer
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    published_by = LoginSerializer(read_only=True)
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['published_by']

