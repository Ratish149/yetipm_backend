from rest_framework import serializers
from .models import (
    State, City, Image, Features,
    FAQ, Project, Testimonial, Inquiry
)

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class FeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    
    class Meta:
        model = City
        fields = '__all__'

class ProjectListDetailSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    features = FeaturesSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'  # Add other fields as necessary

class ProjectSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    features = FeaturesSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.FileField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False,
        allow_empty=True
    )
    feature_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    
    class Meta:
        model = Project
        fields = '__all__'
        extra_kwargs = {
            'slug': {'read_only': True},
        }

    def _is_file(self, data):
        """Helper method to check if the data is a file object"""
        return hasattr(data, 'read') and callable(data.read)

    def _get_valid_files(self, data, field_name):
        """Helper method to extract valid files from request data"""
        if not data:
            return []
            
        if isinstance(data, list):
            return [f for f in data if self._is_file(f)]
            
        if isinstance(data, dict):
            return [f for f in data.values() if self._is_file(f)]
            
        return []

    def create(self, validated_data):
        # Extract and remove many-to-many fields from validated_data
        uploaded_images = validated_data.pop('uploaded_images', [])
        feature_ids = validated_data.pop('feature_ids', [])

        # Create the project instance
        project = Project.objects.create(**validated_data)
        
        # Handle images
        for image_file in self._get_valid_files(uploaded_images, 'uploaded_images'):
            image = Image.objects.create(image=image_file)
            project.images.add(image)
        
        # Handle features
        if feature_ids:
            features = Features.objects.filter(id__in=feature_ids)
            project.features.set(features)
            
        return project

    def update(self, instance, validated_data):
        # Extract and remove many-to-many fields from validated_data
        uploaded_images = validated_data.pop('uploaded_images', [])
        feature_ids = validated_data.pop('feature_ids', [])
        
        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Handle images
        for image_file in self._get_valid_files(uploaded_images, 'uploaded_images'):
            image = Image.objects.create(image=image_file)
            instance.images.add(image)
        
        # Handle features
        if feature_ids is not None:  # Only update if feature_ids is provided
            features = Features.objects.filter(id__in=feature_ids)
            instance.features.set(features)
            
        return instance


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class ProjectAllSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'slug', 'project_address', 
            'price', 'area_square_footage', 'thumbnail_image', 
            'bedrooms', 'bathrooms', 'city','is_featured', 
            'created_at', 'updated_at'
        ]

    def get_images(self, obj):
        """Return only the first image from the images related field."""
        first_image = obj.images.first()
        return ImageSerializer(first_image).data if first_image else None  # Serialize the first image

class InquirySerializer(serializers.ModelSerializer):
    property = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), allow_null=True, required=False)
    class Meta:
        model = Inquiry
        fields = ['id', 'inquiry_type', 'first_name', 'last_name', 'email', 'phone_number', 'message', 'lease_term', 'move_in_date','submitted_at', 'property']
        read_only_fields = ['submitted_at']
        
class InquiryALLSerializer(serializers.ModelSerializer):
    property = ProjectAllSerializer(read_only=True)
    class Meta:
        model = Inquiry
        fields = ['id', 'inquiry_type', 'first_name', 'last_name', 'email', 'phone_number', 'message', 'lease_term', 'move_in_date','submitted_at','property']
        read_only_fields = ['submitted_at']

class WelcomeEmailSerializer(serializers.Serializer):
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        required=True,
    )
    tenant_name = serializers.CharField(
        required=True,
    )
    email = serializers.EmailField(
        required=True,
    )
    rent_due_date = serializers.CharField(
        required=False,

    )
    late_fee_days = serializers.CharField(
        required=False,

    )
    late_fee_amount = serializers.CharField(
        required=False,

    )
    trash_day = serializers.CharField(
        required=False,

    )
    trash_time = serializers.CharField(
        required=False,

    )

    def to_representation(self, instance):
        # This will show all properties in the GET response
        representation = super().to_representation(instance)
        representation['available_properties'] = [
            {
                'id': project.id,
                'name': project.name,
                'address': project.project_address,
                'type': project.project_type,
                'bedrooms': project.bedrooms,
                'bathrooms': project.bathrooms
            }
            for project in Project.objects.all().order_by('name')
        ]
        return representation

class MaintenanceAcknowledgmentSerializer(serializers.Serializer):
    tenant_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

