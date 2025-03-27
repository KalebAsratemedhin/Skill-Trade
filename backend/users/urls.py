from django.urls import path
from .views import CurrentCustomerProfileView, DeleteAccountView, GetAllTechniciansView, GetTechnicianByIdView, RegisterCustomerView, LoginView, LogoutView, RegisterTechnicianView, CurrentTechnicianProfileView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/customer", RegisterCustomerView.as_view(), name="register-customer"),
    path("register/technician", RegisterTechnicianView.as_view(), name="register-technician"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("delete/", DeleteAccountView.as_view(), name="delete"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("current/technician/", CurrentTechnicianProfileView.as_view(), name="technician-profile"),  
    path("current/customer/", CurrentCustomerProfileView.as_view(), name="customer-profile"),
    path("technicians/", GetAllTechniciansView.as_view(), name="all-technicians"),  
    path("technicians/<int:pk>/", GetTechnicianByIdView.as_view(), name="technician by id"),  

]