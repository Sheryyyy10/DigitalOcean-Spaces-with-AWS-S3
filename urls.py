from django.urls import path
from .views import *

urlpatterns = [
    path('spaces/', SpacesView.as_view(), name='spaces-api'),
    path('create_folder/', CreateFolderView.as_view(), name='create_folder'),
]
