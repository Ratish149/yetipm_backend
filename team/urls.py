from django.urls import path
from .views import OurTeamListCreateView,OurTeamRetrieveUpdateDestroyView

urlpatterns = [
    path('team/',OurTeamListCreateView.as_view(),name='ourteam-list-create'),
    path('team/<int:pk>/',OurTeamRetrieveUpdateDestroyView.as_view(),name='ourteam-retrieve-update-destroy'),
]