from django.shortcuts import render
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from .models import (
     State, City, Image,
    FAQ, Project, Testimonial,Inquiry
)
from .serializers import (
    StateSerializer, CitySerializer,
    ImageSerializer,
    FAQSerializer, ProjectSerializer,
    TestimonialSerializer,InquirySerializer
)

# Create your views here.

class StateListCreateView(generics.ListCreateAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'abbreviation']
    filterset_fields = ['name', 'abbreviation']

class StateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    lookup_field = 'slug'

class CityListCreateView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'state__name']
    filterset_fields = ['state']

class CityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'slug'


class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'project_type', 'project_address', 'city__name']
    filterset_fields = {
        'availability': ['exact'],
        'project_type': ['exact'],
        'city': ['exact'],
        'price': ['range'],
        'bedrooms': ['exact', 'gte', 'lte'],
        'bathrooms': ['exact', 'gte', 'lte'],
        'garage_spaces': ['exact', 'gte', 'lte'],
    }
    ordering_fields = ['price', 'name', 'created_at']

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'slug'


class ImageListCreateView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class ImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class InquiryListCreateView(generics.ListCreateAPIView):
    """
    List and create inquiries.
    """
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'email', 'message']
    filterset_fields = ['inquiry_type', 'property']

class InquiryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, and delete a single inquiry.
    """
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer

class TestimonialListCreateView(generics.ListCreateAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'source']

class TestimonialDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
