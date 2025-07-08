from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from rest_framework.views import APIView
from bson import ObjectId

from .models import Patient
from .serializers import PatientSerializer

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from rest_framework.generics import ListCreateAPIView
from rest_framework import mixins, generics

class patients(ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class patient(APIView):
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

class patient(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class PatientViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        try:
            patient = Patient.objects.get(pk=ObjectId(pk))
        except (Patient.DoesNotExist, Exception):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)