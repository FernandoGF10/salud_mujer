from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView

from .models import Patient
from .serializers import PatientSerializer

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from bson import ObjectId


class patients(APIView):
    #@permission_classes([AllowAny])
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

class patient(APIView):
    def get(self, request, object_id):
        try:
            patient = Patient.objects.get(pk=ObjectId(object_id))
        except (Patient.DoesNotExist, Exception):
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = PatientSerializer(patient)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, object_id):
        try:
            patient = Patient.objects.get(pk=ObjectId(object_id))
        except Patient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, object_id):
        try:
            patient = Patient.objects.get(pk=ObjectId(object_id))
        except Patient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)