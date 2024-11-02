from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from django.utils import timezone
from .models import Predictions
from .serializers import PredictionSerializer
from rest_framework.permissions import IsAuthenticated
import requests

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        # Validate the serializer first
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract validated data
        identifier = serializer.validated_data.get('identifier')
        password = serializer.validated_data.get('password')

        # Attempt to authenticate by username, email, or phone number
        user = (
            authenticate(request, username=identifier, password=password) or
            User.objects.filter(email=identifier).first() or
            User.objects.filter(phone_number=identifier).first()
        )

        # Check if the user was found and password matches
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        # Handle invalid credentials
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class PredictView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve all predictions for the authenticated user
        user_predictions = Predictions.objects.filter(user=request.user)
        # Serialize the predictions
        serializer = PredictionSerializer(user_predictions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Validate incoming data
        serializer = PredictionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Get validated data to send for prediction
        validated_data = serializer.validated_data

        # Call the external prediction service
        try:
            response = requests.post("http://127.0.0.1:5000/predict", json=validated_data)
            response_data = response.json()

            # Assume response contains 'stroke_prediction', 'message', 'risk_percentage'
            stroke_prediction = response_data.get('prediction', 0)
            stroke_prediction = True if stroke_prediction == 1 else False
            message = response_data.get('message')
            risk_percentage = float(response_data.get('risk_percentage'))
            
            # Store prediction in database
            prediction = Predictions.objects.create(
                user=request.user,
                gender=validated_data['gender'],
                age=validated_data['age'],
                hypertension=validated_data['hypertension'],
                heart_disease=validated_data['heart_disease'],
                ever_married=validated_data['ever_married'],
                work_type=validated_data['work_type'],
                residence_type=validated_data['residence_type'],
                avg_glucose_level=validated_data['avg_glucose_level'],
                bmi=validated_data['bmi'],
                smoking_status=validated_data['smoking_status'],
                stroke_prediction=stroke_prediction,
                message=message,
                risk_percentage=risk_percentage,
                created_at=timezone.now(),
            )

            # Return the prediction result to the user
            return Response({
                "stroke_prediction": stroke_prediction,
                "message": message,
                "risk_percentage": risk_percentage
            }, status=status.HTTP_201_CREATED)

        except requests.exceptions.RequestException as e:
            # Handle external service errors
            return Response({"error": "Failed to get prediction"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        


