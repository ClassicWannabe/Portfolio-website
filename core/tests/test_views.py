import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Carousel

pytestmark = pytest.mark.django_db


class ProjectViewTests:
    """Tests for `Project` objects view"""

    def test_get_projects_in_order(self, create_project, client, project_url) -> None:
        """Test checking the order of projects"""
        project1 = create_project(order=3, title="project1")
        project2 = create_project(order=1, title="project2")
        project3 = create_project(order=2, title="project3")

        response = client.get(project_url)
        projects = response.context.get("project_list")

        assert response.status_code == 200
        assert len(projects) == 3
        assert projects[0] == project2
        assert projects[1] == project3
        assert projects[2] == project1

    def test_post_not_allowed(self, client, project_url) -> None:
        """Test that POST method is not allowed on project url"""
        payload = {
            "title": "project",
            "source_link": "example.com",
            "demo_link": "example.com",
            "grid_size": 12,
            "order": 2,
        }

        response = client.post(project_url, payload)

        assert response.status_code == 405

    def test_carousel_in_context(self, client, create_project, project_url) -> None:
        """Test that carousel images are in context data of Projects view"""
        create_project(order=1)
        carousel = Carousel.objects.create(
            image=SimpleUploadedFile("img.png", b"content"), published=True, order=1
        )

        response = client.get(project_url)
        carousel_context = response.context.get("carousel")

        assert response.status_code == 200
        assert carousel in carousel_context

    def test_unpublished_carousel_not_in_context(
        self, client, create_project, project_url
    ) -> None:
        """Test that only published carousel images are in context"""
        create_project(order=1)
        carousel1 = Carousel.objects.create(
            image=SimpleUploadedFile("img.png", b"content"), published=True, order=1
        )
        carousel2 = Carousel.objects.create(
            image=SimpleUploadedFile("picture.jpeg", b"content"),
            published=False,
            order=2,
        )

        response = client.get(project_url)
        carousel_context = response.context.get("carousel")

        assert response.status_code == 200
        assert carousel1 in carousel_context
        assert carousel2 not in carousel_context


class AboutViewTests:
    """Tests for `About` objects view"""

    def test_get_unpublished_about_returns_404(
        self, client, create_about, about_url
    ) -> None:
        """Test getting about page returns Not Found because of unpublished page"""
        create_about()
        create_about()

        response = client.get(about_url)
        context = response.context.get("about")

        assert context is None
        assert response.status_code == 404

    def test_get_published_about_successful(
        self, client, create_about, about_url
    ) -> None:
        """Test getting about page is successful"""
        about = create_about(published=True)

        response = client.get(about_url)
        context = response.context.get("about")

        assert response.status_code == 200
        assert context == about


class ContactsViewTests:
    """Tests for `Contacts` objects view"""

    def test_get_unpublished_contacts_returns_404(
        self, client, create_contacts, contacts_url
    ) -> None:
        """Test getting contacts page returns Not Found because of unpublished page"""
        create_contacts()
        create_contacts()

        response = client.get(contacts_url)
        context = response.context.get("contacts")

        assert context is None
        assert response.status_code == 404

    def test_get_published_contacts_successful(
        self, client, create_contacts, contacts_url
    ) -> None:
        """Test getting contacts page is successful"""
        contacts = create_contacts(published=True)

        response = client.get(contacts_url)
        context = response.context.get("contacts")

        assert response.status_code == 200
        assert context == contacts
