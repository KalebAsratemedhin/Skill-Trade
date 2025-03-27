from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import Booking
from .serializers import BookingSerializer, CreateBookingSerializer, UpdateBookingSerializer

class BookingListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: BookingSerializer(many=True)},
    )
    def get(self, request):
        # Get all bookings for the authenticated user (either as customer or technician)
        bookings = Booking.objects.filter(
            customer=request.user
        ) | Booking.objects.filter(technician=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CreateBookingSerializer,
        responses={201: BookingSerializer()},
    )
    def post(self, request):
        data = request.data 
        data["customer"] = request.user.id
        serializer = CreateBookingSerializer(data=data)
        

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: BookingSerializer()},
    )
    def get(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
            if booking.customer != request.user and booking.technician != request.user:
                return Response({"error": "You do not have permission to view this booking."},
                                status=status.HTTP_403_FORBIDDEN)
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=UpdateBookingSerializer,
        responses={200: BookingSerializer()},
    )
    def put(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
            if booking.customer != request.user and booking.technician != request.user:
                return Response({"error": "You do nnot have permission to update this booking."},
                                status=status.HTTP_403_FORBIDDEN)

            data = request.data
            serializer = BookingSerializer(booking, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=BookingSerializer,
        responses={204: "Booking deleted successfully."},
    )
    def delete(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
            if booking.customer != request.user and booking.technician != request.user:
                return Response({"error": "You do not have permission to delete this booking."},
                                 status=status.HTTP_403_FORBIDDEN)

            booking.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)  # No content is needed for delete operation
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
