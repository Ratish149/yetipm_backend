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
    property_type = django_filters.CharFilter(field_name="project_type", lookup_expr='iexact')
    city = django_filters.CharFilter(field_name="city__id", lookup_expr='iexact')
    min_area_square_footage = django_filters.NumberFilter(field_name="area_square_footage", lookup_expr='gte')
    max_area_square_footage = django_filters.NumberFilter(field_name="area_square_footage", lookup_expr='lte')
    features = django_filters.ModelMultipleChoiceFilter(queryset=Features.objects.all(), field_name='features')
    
    class Meta:
        model = Project
        fields = ['min_price', 'max_price', 'beds', 'baths', 'property_type', 'city', 'min_area_square_footage', 'max_area_square_footage', 'features']

class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.filter(availability=True).order_by('-created_at')
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
        inquiry_type = inquiry_data.get('inquiry_type')  # Get the inquiry type
        property_details = inquiry_data.get('property') if 'property' in inquiry_data else None
        
        # Send emails based on inquiry type
        if inquiry_type == 'Specific Property':
            self.send_user_email(recipient_email, inquiry_data, property_details)  # Send user email
        elif inquiry_type == 'General Inquiry':  # New condition for General Inquiry
            self.send_general_inquiry_email(recipient_email, inquiry_data)  # Send general inquiry email
        self.send_admin_email(inquiry_data, property_details)  # Always send admin email
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def send_user_email(self, email, inquiry_data, property_details):
        # Get the property address from the property object
        property_address = None
        if property_details:
            property = Project.objects.get(id=property_details)
            property_slug = property.slug
            property_address = property.project_address  # Get the property address
            property_price = property.price

        else:
            property_slug = None
        
        subject = f"Availability Inquiry for {property_address}"

        message = render_to_string('email/user_email_template.html', {
            'first_name': inquiry_data['first_name'],
            'last_name': inquiry_data['last_name'],
            'email': inquiry_data['email'],
            'phone_number': inquiry_data['phone_number'],
            'message': inquiry_data['message'],
            'lease_term': inquiry_data['lease_term'],  
            'move_in_date': inquiry_data['move_in_date'],
            'property_price': property_price, 
            'property_address': property_address,
            'property': property_slug
        })
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list, html_message=message)

    def send_admin_email(self, inquiry_data, property_details):
        property_address = None
        if property_details:
            property = Project.objects.get(id=property_details)
            property_slug = property.slug
            property_address = property.project_address  
            property_price = property.price
            subject = f"New Inquiry Notification for {property_address}"  # Subject with property address
        else:
            subject = "New General Inquiry Notification"  # Subject without property address

        message = render_to_string('email/email_template.html', {
            'first_name': inquiry_data['first_name'],
            'last_name': inquiry_data['last_name'],
            'email': inquiry_data['email'],
            'phone_number': inquiry_data['phone_number'],
            'message': inquiry_data['message'],
            'property': property_details  # Pass property details if available
        })
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [settings.EMAIL_HOST_USER]  # Replace with the actual admin email

        send_mail(subject, message, from_email, recipient_list, html_message=message)

    def send_general_inquiry_email(self, email, inquiry_data):
        subject = "General Inquiry Response"
        message = render_to_string('email/general_inquiry_template.html', {
            'first_name': inquiry_data['first_name'],
            'last_name': inquiry_data['last_name'],
        })
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

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
    filter_backends = [rest_filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['question']
    filterset_fields = ['category']
    pagination_class = None  # This will remove pagination for this view

class FAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    lookup_field = 'id'  # Assuming you want to look up by a slug field
