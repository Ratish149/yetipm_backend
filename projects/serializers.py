from rest_framework import serializers
from .models import (
    State, City, Image,
    FAQ, Project, Testimonial,Inquiry
)

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
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

class ProjectSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.FileField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False,
        allow_empty=True
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
        # Extract and validate files
        uploaded_images = self._get_valid_files(validated_data.pop('uploaded_images', []), 'uploaded_images')

        project = Project.objects.create(**validated_data)
        
        # Handle images
        for image_file in uploaded_images:
            image = Image.objects.create(image=image_file)
            project.images.add(image)
            
            
        return project

    def update(self, instance, validated_data):
        # Extract and validate files
        uploaded_images = self._get_valid_files(validated_data.pop('uploaded_images', []), 'uploaded_images')

        
        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Handle images
        for image_file in uploaded_images:
            image = Image.objects.create(image=image_file)
            instance.images.add(image)
            
            
        return instance

class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = [
            'id', 'inquiry_type', 'property', 'name', 'email', 'message', 'submitted_at'
        ]
        read_only_fields = ['submitted_at']

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'
