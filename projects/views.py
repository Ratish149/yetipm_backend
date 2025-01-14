from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters as rest_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters import rest_framework as django_filters
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings  # Import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


from .models import (
    State, City, Image, Features,
    FAQ, Project, Testimonial, Inquiry
)
from .serializers import (
    StateSerializer, CitySerializer, ImageSerializer,
    FeaturesSerializer, FAQSerializer, ProjectSerializer,
    TestimonialSerializer, InquirySerializer
)

# Create your views here.

class StateListCreateView(generics.ListCreateAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    filter_backends = [rest_filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'abbreviation']
    filterset_fields = ['name', 'abbreviation']

class StateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    lookup_field = 'slug'

class CityListCreateView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [rest_filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'state__name']
    filterset_fields = ['state']

class CityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'slug'

class FeaturesListCreateView(generics.ListCreateAPIView):
    queryset = Features.objects.all()
    serializer_class = FeaturesSerializer
    parser_classes = (MultiPartParser, FormParser)

class FeaturesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Features.objects.all()
    serializer_class = FeaturesSerializer
    parser_classes = (MultiPartParser, FormParser)

class ProjectFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    beds = django_filters.NumberFilter(field_name="bedrooms", lookup_expr='gte')
    baths = django_filters.NumberFilter(field_name="bathrooms", lookup_expr='gte')
    property_type = django_filters.CharFilter(field_name="property_type", lookup_expr='iexact')
    city = django_filters.CharFilter(field_name="city__name", lookup_expr='iexact')
    
    class Meta:
        model = Project
        fields = ['min_price', 'max_price', 'beds', 'baths', 'property_type', 'city']

class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    filterset_class = ProjectFilter
    filter_backends = [DjangoFilterBackend, rest_filters.SearchFilter, rest_filters.OrderingFilter]
    search_fields = ['name', 'project_address', 'city__name']
    ordering_fields = ['price', 'created_at']
    parser_classes = (MultiPartParser, FormParser)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Handle availability filter separately
        availability = self.request.query_params.get('availability')
        if availability is not None:
            # Convert string to boolean
            is_available = availability.lower() in ['true', '1', 'yes']
            queryset = queryset.filter(availability=is_available)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            print(f"Error in ProjectListView create: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'slug'

class ImageListCreateView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)

class ImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class InquiryListCreateView(generics.ListCreateAPIView):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
    filter_backends = [rest_filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['first_name', 'last_name', 'email']
    filterset_fields = ['inquiry_type', 'property']

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        # Send confirmation email
        inquiry_data = response.data
        self.send_confirmation_email(inquiry_data['email'], inquiry_data['first_name'])
        
        return response

    def send_confirmation_email(self, email, first_name):
        subject = "Inquiry Confirmation"
        message = render_to_string('email/email_template.html', {'first_name': first_name})
        from_email = settings.DEFAULT_FROM_EMAIL  # Use the default email from settings
        recipient_list = [email]

        # Send the email
        send_mail(subject, message, from_email, recipient_list, html_message=message)

class InquiryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer

class TestimonialListCreateView(generics.ListCreateAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [rest_filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'testimonial']
    filterset_fields = ['source']

class TestimonialDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer

class ProjectCityListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    filterset_class = ProjectFilter
    filter_backends = [DjangoFilterBackend, rest_filters.SearchFilter, rest_filters.OrderingFilter]
    search_fields = ['name', 'project_address']
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        city_slug = self.kwargs['city_slug']
        queryset = Project.objects.filter(city__slug=city_slug).order_by('-created_at')
        
        # Handle availability filter
        availability = self.request.query_params.get('availability')
        if availability is not None:
            is_available = availability.lower() in ['true', '1', 'yes']
            queryset = queryset.filter(availability=is_available)
        
        return queryset
