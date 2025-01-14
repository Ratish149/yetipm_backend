from django.urls import path
from . import views

urlpatterns = [
    # State URLs
    path('states/', views.StateListCreateView.as_view(), name='state-list'),
    path('states/<slug:slug>/', views.StateDetailView.as_view(), name='state-detail'),
    
    # City URLs
    path('cities/', views.CityListCreateView.as_view(), name='city-list'),
    path('cities/<slug:slug>/', views.CityDetailView.as_view(), name='city-detail'),
    
    # Features URLs
    path('features/', views.FeaturesListCreateView.as_view(), name='features-list'),
    path('features/<int:pk>/', views.FeaturesDetailView.as_view(), name='features-detail'),
    
    # Project URLs
    path('projects/', views.ProjectListView.as_view(), name='project-list'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project-detail'),
    
    # Image URLs
    path('images/', views.ImageListCreateView.as_view(), name='image-list'),
    path('images/<int:pk>/', views.ImageDetailView.as_view(), name='image-detail'),
    
    # Inquiry URLs
    path('inquiries/', views.InquiryListCreateView.as_view(), name='inquiry-list'),
    path('inquiries/<int:pk>/', views.InquiryDetailView.as_view(), name='inquiry-detail'),
    
    # Testimonial URLs
    path('testimonials/', views.TestimonialListCreateView.as_view(), name='testimonial-list'),
    path('testimonials/<int:pk>/', views.TestimonialDetailView.as_view(), name='testimonial-detail'),
    
    path('projects/city/<slug:city_slug>/', views.ProjectCityListView.as_view(), name='project-city-list'),
]
