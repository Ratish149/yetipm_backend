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
from rest_framework.pagination import PageNumberPagination
from .serializers import (
    StateSerializer, CitySerializer, ImageSerializer,
    FeaturesSerializer, FAQSerializer, ProjectSerializer,
    TestimonialSerializer, InquirySerializer, ProjectAllSerializer,ProjectListDetailSerializer, InquiryALLSerializer
)

# Create your views here.

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class StateListCreateView(generics.ListCreateAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    filter_backends = [rest_filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'abbreviation']
    filterset_fields = ['name', 'abbreviation']
    pagination_class = CustomPagination

class StateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    lookup_field = 'slug'

class CityListCreateView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [rest_filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['state', 'name']
    pagination_class = CustomPagination

class CityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'slug'

class FeaturesListCreateView(generics.ListCreateAPIView):
    queryset = Features.objects.all()
    serializer_class = FeaturesSerializer
    parser_classes = (MultiPartParser, FormParser)
    pagination_class = CustomPagination

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
    city = django_filters.CharFilter(field_name="city__name", lookup_expr='icontains')
    min_area_square_footage = django_filters.NumberFilter(field_name="area_square_footage", lookup_expr='gte')
    max_area_square_footage = django_filters.NumberFilter(field_name="area_square_footage", lookup_expr='lte')
    features = django_filters.ModelMultipleChoiceFilter(queryset=Features.objects.all(), field_name='features')
    
    class Meta:
        model = Project
        fields = ['min_price', 'max_price', 'beds', 'baths', 'property_type', 'city', 'min_area_square_footage', 'max_area_square_footage', 'features']

class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectAllSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProjectSerializer
        return super().get_serializer_class()

    filterset_class = ProjectFilter
    filter_backends = [DjangoFilterBackend, rest_filters.SearchFilter, rest_filters.OrderingFilter]
    search_fields = ['name', 'project_address', 'city__name']
    ordering_fields = ['price', 'created_at']
    parser_classes = (MultiPartParser, FormParser)
    pagination_class = CustomPagination
    
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
    serializer_class = ProjectListDetailSerializer
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
    queryset = Inquiry.objects.all().order_by('-submitted_at')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return InquirySerializer
        return InquiryALLSerializer  # Use InquiryALLSerializer for GET requests

    serializer_class = InquirySerializer  # Default serializer for POST requests
    filter_backends = [rest_filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['first_name', 'last_name', 'email']
    filterset_fields = ['inquiry_type', 'property']

    def create(self, request, *args, **kwargs):
        # Use the serializer to validate and create the Inquiry instance
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the Inquiry instance, which will include the property
        inquiry_instance = serializer.save()

        # Send confirmation email
        inquiry_data = serializer.data
        
        # Determine the recipient email based on inquiry type
        recipient_email = inquiry_data.get('email')
        
        # Check if property details are available
        property_details = inquiry_data.get('property') if 'property' in inquiry_data else None
        
        self.send_confirmation_email(recipient_email, inquiry_data, property_details)  # Pass property details if available
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def send_confirmation_email(self, email, inquiry_data, property_details):
        subject = "Inquiry Confirmation"        
        # Check if property_details is provided
        if property_details:
            property = Project.objects.get(id=property_details)
            property_slug = property.slug
        else:
            property_slug = None  # Set to None if no property details are provided

        message = render_to_string('email/email_template.html', {
            'first_name': inquiry_data['first_name'],
            'last_name': inquiry_data['last_name'],
            'email': inquiry_data['email'],
            'phone_number': inquiry_data['phone_number'],
            'message': inquiry_data['message'],
            'property': property_slug  # Pass property details or None
        })
        from_email = settings.DEFAULT_FROM_EMAIL  # Use the default email from settings
        recipient_list = [email]

        # Send the email
        send_mail(subject, message, from_email, recipient_list, html_message=message)

class InquiryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inquiry.objects.all()
    serializer_class = InquiryALLSerializer

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

class FAQListCreateView(generics.ListCreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    parser_classes = (MultiPartParser, FormParser)
    pagination_class = CustomPagination
    filter_backends = [rest_filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['question']  # Assuming you want to search by the question field

class FAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    lookup_field = 'id'  # Assuming you want to look up by a slug field
