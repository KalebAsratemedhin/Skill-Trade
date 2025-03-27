from django.urls import path
from .views import BookingListView, BookingDetailView, BookingStatusUpdateView

urlpatterns = [
    path('', BookingListView.as_view(), name='booking-list'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('status-update/<int:pk>/', BookingStatusUpdateView.as_view(), name='booking-status-update'),
]
