from django.urls import path
from .views import CurrentUserProfileView, DeleteAccountView, GetAllTechniciansView, GetTechnicianByIdView, LoginView, LogoutView, RegisterView, SendEmailVerificationView, VerifyEmailView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register", RegisterView.as_view(), name="register-customer"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("delete", DeleteAccountView.as_view(), name="delete"),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("current", CurrentUserProfileView.as_view(), name="technician-profile"),  
    path("technicians", GetAllTechniciansView.as_view(), name="all-technicians"),  
    path("technicians/<int:pk>", GetTechnicianByIdView.as_view(), name="technician by id"),  
    path("verify-email/<str:token>", VerifyEmailView.as_view(), name="verify-email"),
    path("send-verification-email", SendEmailVerificationView.as_view(), name="verify-email"),

]