from asyncio import QueueEmpty
from django.shortcuts import render
from html5lib import serialize
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Question
from .serializer import QuestionSerializer
from rest_framework import status
# Create your views here.

class QuestionList(APIView):
    def get(self, request):
        question = Question.objects.all()
        serialize = QuestionSerializer(question, many=True)
        return Response(serialize.data, status=status.HTTP_200_OK)

class CreateQuestion(APIView):
    def post(self, request):
        question = request.data
        serialize = QuestionSerializer(data = question)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_201_CREATED)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateQuestion(APIView):
    def get(self, request, id):
        try:
            question = Question.objects.get(pk=id)
        except Question.DoesNotExist:
            return Response({'error':'question does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serialize = QuestionSerializer(question)
        return Response(serialize.data, status = status.HTTP_200_OK)
    
    def put(self, request, id):
        try:
            question = Question.objects.get(pk=id)
        except Question.DoesNotExist:
            return Response({'error':'question does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serialize = QuestionSerializer(question, data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_200_OK)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        question = Question.objects.get(pk=id)
        question.delete()
        return Response({'status':'Question deleted successfully'}, status=status.HTTP_204_NO_CONTENT)