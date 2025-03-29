from users.utils import send_verification_email
from users.permissions import IsCustomer, IsTechnician
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg import openapi
from .serializers import CustomerSerializer, TechnicianSerializer, UpdateCustomerSerializer, UpdateTechnicianSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import EmailVerificationToken, User, TechnicianProfile
class RegisterCustomerView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=CustomerSerializer,
        responses={201: CustomerSerializer}
    )
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)  

            return Response({
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class RegisterTechnicianView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=TechnicianSerializer,
        responses={201: TechnicianSerializer}
    )
    def post(self, request):
        serializer = TechnicianSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)  
            return Response({
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: openapi.Response("Login successful", LoginSerializer)},
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(username=serializer.validated_data["username"])
            refresh = RefreshToken.for_user(user)  
            return Response({
                "message": "Login successful",
                "user": serializer.validated_data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class GetTechnicianByIdView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: TechnicianSerializer()},
        security=[{'Bearer': []}] 
    )
    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk, role="technician")
            serializer = TechnicianSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TechnicianProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
class GetAllTechniciansView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        responses={200: TechnicianSerializer()},
        security=[{'Bearer': []}] 
    )
    def get(self, request):
        try:
            technicians = User.objects.filter(role="technician")
            serializer = TechnicianSerializer(technicians, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TechnicianProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
class CurrentTechnicianProfileView(APIView):
    permission_classes = [IsAuthenticated, IsTechnician]

    @swagger_auto_schema(
        responses={200: TechnicianSerializer()},
        security=[{'Bearer': []}]

    )
    def get(self, request):
        try:
            serializer = TechnicianSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TechnicianProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
 
    
    @swagger_auto_schema(
        request_body=UpdateTechnicianSerializer, 
        responses={200: TechnicianSerializer()},
        security=[{'Bearer': []}]

    )
    def put(self, request):
        try:
            serializer = UpdateTechnicianSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                new_user = User.objects.get(id=request.user.id)
                serializer = TechnicianSerializer(new_user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TechnicianProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
class CurrentCustomerProfileView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    @swagger_auto_schema(
        responses={200: CustomerSerializer()},
        security=[{'Bearer': []}]
    )
    def get(self, request):
        serializer = CustomerSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UpdateCustomerSerializer,
        responses={200: UpdateCustomerSerializer()},
        security=[{'Bearer': []}]
    )
    def put(self, request):
        serializer = UpdateCustomerSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh": openapi.Schema(type=openapi.TYPE_STRING, description="Refresh token")
            },
            required=["refresh"]
        ),
        responses={200: openapi.Response("Logged out successfully")},
    )
    def post(self, request):
        """Logout by blacklisting the refresh token"""
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: openapi.Response("Account deleted successfully")}
    )
    def delete(self, request):
        """Delete the authenticated user's account"""
        user = request.user
        user.delete()
        return Response({"message": "Account deleted successfully"}, status=status.HTTP_200_OK)

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            verification_token = EmailVerificationToken.objects.get(token=token)

            if verification_token.is_expired():
                return Response("Verification link expired", status=400)

            user = verification_token.user
            user.is_verified = True 
            user.save()
            verification_token.delete()
            return Response("Email verified successfully", status=200)

        except EmailVerificationToken.DoesNotExist:
            return Response("Invalid verification link", status=400)

class ResendEmailVerificationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user = request.user
        send_verification_email(user)
        return Response("Verification email sent successfully", status=200)