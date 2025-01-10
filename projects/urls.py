from django.urls import path
from . import views

urlpatterns = [
    path('states/', views.StateListCreateView.as_view(), name='state-list'),
    path('states/<slug:slug>/', views.StateDetailView.as_view(), name='state-detail'),
    
    path('cities/', views.CityListCreateView.as_view(), name='city-list'),
    path('cities/<slug:slug>/', views.CityDetailView.as_view(), name='city-detail'),
        
    path('projects/', views.ProjectListCreateView.as_view(), name='project-list'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project-detail'),
    
    path('images/', views.ImageListCreateView.as_view(), name='image-list'),
    path('images/<int:pk>/', views.ImageDetailView.as_view(), name='image-detail'),

    path('testimonials/', views.TestimonialListCreateView.as_view(), name='testimonial-list'),
    path('testimonials/<int:pk>/', views.TestimonialDetailView.as_view(), name='testimonial-detail'),

    path('inquiries/', views.InquiryListCreateView.as_view(), name='inquiry-list'),
    path('inquires/<int:pk>/', views.InquiryDetailView.as_view(), name='inquiry-detail'),

]
