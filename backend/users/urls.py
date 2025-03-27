from django.urls import path
from .views import CustomerProfileView, DeleteAccountView, RegisterCustomerView, LoginView, LogoutView, RegisterTechnicianView, TechnicianProfileView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/customer", RegisterCustomerView.as_view(), name="register-customer"),
    path("register/technician", RegisterTechnicianView.as_view(), name="register-technician"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("delete/", DeleteAccountView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("profile/technician/", TechnicianProfileView.as_view(), name="technician-profile"),  
    path("profile/customer/", CustomerProfileView.as_view(), name="customer-profile"),  

]