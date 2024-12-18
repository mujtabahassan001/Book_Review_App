from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Books.urls')),
    path('', include('Auth.urls')),
    path('', include('Comments.urls')),
    path('', include('Reviews.urls'))
]
