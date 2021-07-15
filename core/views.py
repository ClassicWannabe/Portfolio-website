from django.views.generic import TemplateView, ListView, DetailView

from .utils import GetPublishedPageMixin

from .models import Project, About, Contacts


class HomeView(TemplateView):
    template_name = "home.html"


class AboutView(GetPublishedPageMixin, DetailView):
    model = About
    template_name = "about.html"


class ProjectsView(ListView):
    model = Project
    template_name = "projects.html"


class ContactsView(GetPublishedPageMixin, DetailView):
    model = Contacts
    template_name = "contacts.html"
