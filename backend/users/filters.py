
from django_filters import rest_framework as filters
from users.models import User
from rest_framework.pagination import PageNumberPagination

class TechnicianFilter(filters.FilterSet):
    expertise = filters.CharFilter(field_name="technicianprofile__expertise", lookup_expr='icontains')
    experience_years = filters.NumberFilter(field_name="technicianprofile__experience_years", lookup_expr="above")
    username = filters.CharFilter(field_name="username", lookup_expr="icontains") 


class TechnicianPagination(PageNumberPagination):
    page_size = 2  
    page_size_query_param = 'page_size'  
    max_page_size = 50 

