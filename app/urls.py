from django.urls import path
from .views import HomeView, ProjectsView, AboutView

app_name = 'app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about', AboutView.as_view(), name='about'),
    path('projects', ProjectsView.as_view(), name='projects'),
    path('contacts', ProjectsView.as_view(), name='contacts'),
]