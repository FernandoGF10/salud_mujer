from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            '_id',
            'first_name',
            'last_name',
            'run',
            'email',
            'phone',
            'birth_date',
            'gender',
            'region',
            'city',
            'address',
            'health_provider',
            'created_at',
            'updated_at',
        ]

    def get__id(self, obj):
        return str(obj._id)