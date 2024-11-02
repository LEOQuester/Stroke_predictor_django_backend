from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import Predictions

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)





class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predictions
        fields = [
            'gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 
            'work_type', 'residence_type', 'avg_glucose_level', 'bmi', 'smoking_status','created_at','stroke_prediction', 'message', 'risk_percentage',
        ]

