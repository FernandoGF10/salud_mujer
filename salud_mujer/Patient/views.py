# Imports estándar de Python
from django.shortcuts import render
from django.http import JsonResponse
from bson import ObjectId

# Imports de terceros (Django REST Framework)
from rest_framework import status, viewsets, mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView

# Imports locales
from .models import Patient
from .serializers import PatientSerializer

# --- Generic View: Listar todos los pacientes ---
class patients(ListCreateAPIView):
    """Vista genérica para listar todos los pacientes (GET /patients/)."""
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

# --- APIView: Obtener, actualizar y eliminar paciente por ID ---
class patient(APIView):
    """Vista basada en clase para actualizar (PUT) y eliminar (DELETE) un paciente por su ObjectId."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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

# --- Mixin: Crear paciente (solo POST) ---
class PatientMixin(mixins.CreateModelMixin, generics.GenericAPIView):
    """Vista basada en Mixin para crear un paciente (POST /patient/)."""
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
# --- ViewSet: Obtener paciente por ID (GET) ---
class PatientViewSet(viewsets.ViewSet):
    """ViewSet para obtener un paciente por su ObjectId (GET /viewset/patient/<id>/)."""
    def retrieve(self, request, pk=None):
        try:
            patient = Patient.objects.get(pk=ObjectId(pk))
        except (Patient.DoesNotExist, Exception):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)