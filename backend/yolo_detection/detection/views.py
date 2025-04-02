# views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .serializer import FolderDetectionSerializer
import torch
import os

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

class FolderDetectionView(generics.GenericAPIView):
    parser_classes = [JSONParser]
    serializer_class = FolderDetectionSerializer  # Using Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # Validate input data
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        folder_path = serializer.validated_data['folder_path']

        # Check folder path existence
        if not os.path.exists(folder_path):
            return Response({"error": "Folder path does not exist"}, status=400)

        # Detect objects
        detected_files = self.detect_objects_in_folder(folder_path)
        return Response({"detected_files": detected_files})

    def detect_objects_in_folder(self, folder_path):
        """Helper method for object detection in folder"""
        detected_files = []

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                results = model(file_path)
                labels = results.pandas().xyxy[0]['name'].tolist()

                # Append detected files
                if 'dog' in labels or 'cat' in labels:
                    detected_files.append(filename)

        return detected_files
