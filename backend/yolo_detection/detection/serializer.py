# serializers.py
from rest_framework import serializers

class FolderDetectionSerializer(serializers.Serializer):
    folder_path = serializers.CharField(required=True)
