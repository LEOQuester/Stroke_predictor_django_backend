from django.urls import path
from .views import RegisterView, LoginView, PredictView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('predict/', PredictView.as_view(), name='predict'),
]
