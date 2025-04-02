from django.urls import path
from .views import *

urlpatterns = [
    path('detect/', FolderDetectionView.as_view(), name='object-detection'),
]
