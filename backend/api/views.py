
from django.contrib.auth.models import User
from .models import Note
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer, NoteSerializer, AnswerSerializer
from dotenv import load_dotenv
import requests
from rest_framework.permissions import IsAuthenticated, AllowAny
import os
from django.http import JsonResponse
import google.generativeai as genai
from decouple import config

load_dotenv()
class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)

class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    persmission_classes = [AllowAny]

class AnswerView(generics.CreateAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [AllowAny]


    def post(self, request):
        data = request.data.get('data')
        print(data)
        
        try:
            question_api_key = os.getenv('API_KEY_FOR_USER')
            response = requests.post(f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={question_api_key}', json={
                "contents": data
            })

            return JsonResponse(response.json())
        except:
            return JsonResponse({'error': 'An error occurred while processing your request.'})