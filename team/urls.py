from django.urls import path
from .views import OurTeamListCreateView,OurTeamRetrieveUpdateDestroyView

urlpatterns = [
    path('',OurTeamListCreateView.as_view(),name='ourteam-list-create'),
    path('<int:pk>/',OurTeamRetrieveUpdateDestroyView.as_view(),name='ourteam-retrieve-update-destroy'),
]