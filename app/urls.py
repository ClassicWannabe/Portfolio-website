from django.urls import path
from .views import HomeView, ProjectsView

app_name = 'app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('projects', ProjectsView.as_view(), name='projects'),
    path('projects', ProjectsView.as_view(), name='contacts'),
]