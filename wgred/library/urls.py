from django.urls import path
from .views import index, by_file


urlpatterns = [
    path('<int:file_id>/', by_file, name='by_file'),
    path('', index, name='index'),
]
