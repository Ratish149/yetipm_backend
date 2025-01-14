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

class ProjectSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    features = FeaturesSerializer(many=True, read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)
    city = CitySerializer(read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.FileField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Project
        fields = '__all__'
        extra_kwargs = {
            'slug': {'read_only': True},
        }

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        project = Project.objects.create(**validated_data)
        
        for image_file in uploaded_images:
            image = Image.objects.create(image=image_file)
            project.images.add(image)
        
        return project

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        for image_file in uploaded_images:
            image = Image.objects.create(image=image_file)
            instance.images.add(image)
        
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
