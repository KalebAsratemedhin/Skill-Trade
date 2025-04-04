from users.filters import TechnicianFilter, TechnicianPagination
from users.utils import send_verification_email
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg import openapi
from .serializers import UpdateUserSerializer, UserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import EmailVerificationToken, User, TechnicianProfile
class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={201: UserSerializer}
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
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
        responses={200: UserSerializer()},
        security=[{'Bearer': []}] 
    )
    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk, role="technician")
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

class GetAllTechniciansView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'expertise',
                openapi.IN_QUERY,
                description="Filter by expertise (e.g., Plumbing, Electrical)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'experience',
                openapi.IN_QUERY,
                description="Filter by experience (years)",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description="Search by name (case insensitive)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Page number for pagination",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description="Number of items per page",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={200: UserSerializer(many=True)},
        security=[{'Bearer': []}]
    )
    def get(self, request):
        try:
            technicians = User.objects.filter(role="technician").select_related("technicianprofile")
            
            
            filterset = TechnicianFilter(request.GET, queryset=technicians)
            if filterset.is_valid():
                technicians = filterset.qs

            paginator = TechnicianPagination()
            paginated_technicians = paginator.paginate_queryset(technicians, request)
            serializer = UserSerializer(paginated_technicians, many=True)
            
            return paginator.get_paginated_response(serializer.data)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class CurrentUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: UserSerializer()},
        security=[{'Bearer': []}]
    )
    def get(self, request):
        try:
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
 
    
    @swagger_auto_schema(
        request_body=UpdateUserSerializer, 
        responses={200: UserSerializer()},
        security=[{'Bearer': []}]

    )
    def put(self, request):
        try:
            serializer = UpdateUserSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                new_user = User.objects.get(id=request.user.id)
                serializer = UserSerializer(new_user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        

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

class SendEmailVerificationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user = request.user
        send_verification_email(user)
        return Response("Verification email sent successfully", status=200)