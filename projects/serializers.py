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
    state=StateSerializer(read_only=True)
    
    class Meta:
        model = City
        fields = '__all__'

class ProjectListDetailSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(read_only=True)
    features = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    images = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'slug', 'city', 'features', 'images', 'price', 'availability']  # Add other fields as necessary

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
    city_detail = CitySerializer(source='city', read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'slug', 'project_type', 'project_address', 
            'price', 'price_breakdown', 'project_description', 
            'area_square_footage', 'garage_spaces', 'images', 
            'features', 'bedrooms', 'bathrooms', 'city', 'city_detail',
            'availability', 'avialable_date', 'postal_code', 'uploaded_images',
            'feature_ids', 'created_at', 'updated_at'
        ]
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

class InquirySerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(source='property.name', read_only=True)
    
    class Meta:
        model = Inquiry
        fields = '__all__'
        read_only_fields = ['submitted_at']

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class ProjectDetailSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    features = FeaturesSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'slug', 'project_type', 'project_address', 
            'price','area_square_footage', 'garage_spaces', 'images', 
            'features', 'bedrooms', 'bathrooms', 'city', 
            'availability', 'avialable_date', 'postal_code', 
            'created_at', 'updated_at'
        ]
