from typing import Any

from django.views.generic import TemplateView, ListView, DetailView

from .utils import GetPublishedPageMixin
from .models import Project, About, Contacts, Carousel


class HomeView(TemplateView):
    template_name = "home.html"


class AboutView(GetPublishedPageMixin, DetailView):
    model = About
    template_name = "about.html"


class ProjectsView(ListView):
    model = Project
    template_name = "projects.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add extra context to the existing one"""
        context = super().get_context_data(**kwargs)
        context["carousel"] = Carousel.objects.filter(published=True)

        return context


class ContactsView(GetPublishedPageMixin, DetailView):
    model = Contacts
    template_name = "contacts.html"
