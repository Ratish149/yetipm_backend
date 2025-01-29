from django.shortcuts import render
from rest_framework import generics
from .models import OurTeam
from .serializers import OurTeamSerializer

# Create your views here.

class OurTeamListCreateView(generics.ListCreateAPIView):
    queryset = OurTeam.objects.all().order_by('created_at')
    serializer_class = OurTeamSerializer

class OurTeamRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OurTeam.objects.all()
    serializer_class = OurTeamSerializer

