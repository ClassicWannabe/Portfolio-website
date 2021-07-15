import os

import pytest

from django.db.utils import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

from ..models import Project, About, Document, Contacts, Link

pytestmark = pytest.mark.django_db


class ProjectModelTests:
    """Tests for `Project` model"""

    def test_create_project_successful(self, create_project) -> None:
        """Test creating projects in the DB is successful"""
        project1 = create_project(order=1, title="My first project")
        project2 = create_project(order=2, title="My second project")

        projects = Project.objects.all()
        assert projects[0] == project1
        assert projects[1] == project2

    def test_project_str(self, create_project) -> None:
        """Test the project string representation"""
        project = create_project(order=1, title="My project")

        assert str(project) == project.title

    def test_project_unique_fields_fails(self, create_project) -> None:
        """Test creating project with non-unique fields fails"""
        with pytest.raises(IntegrityError):
            create_project(order=1, source_link="example.com")
            create_project(order=1, source_link="example.com")

    def test_delete_project_with_picture(self, create_project) -> None:
        """Test deleting a project also deletes project picture"""
        project = create_project(order=1, filename="mypicture")
        picture_path = project.picture.path
        project.delete()

        assert not os.path.exists(picture_path)

    def test_update_project_picture(self, create_project) -> None:
        """Test updating a project picture deletes an old picture"""
        project = create_project(order=1, filename="my-beatiful-picture")
        old_picture_path = project.picture.path
        new_picture = SimpleUploadedFile("new_picture.png", b"content")
        project.picture = new_picture
        project.save()
        new_picture_path = project.picture.path

        assert not os.path.exists(old_picture_path)
        assert os.path.exists(new_picture_path)


class AboutModelTests:
    """Test for `About` model"""

    def test_create_about_successful(self, create_about) -> None:
        """Test creating `About` objects is successful"""
        about1 = create_about()
        about2 = create_about()

        abouts = About.objects.all()

        assert about1 in abouts
        assert about2 in abouts

    def test_about_str(self, create_about) -> None:
        """Test `About` object string representation"""
        about = create_about(title="Title Title")

        assert str(about) == about.title

    def test_create_about_published_fails(self, create_about) -> None:
        """Test creating more than one published about raises ValidationError"""
        with pytest.raises(ValidationError):
            create_about(published=True)
            create_about(published=True)


class DocumentModelTests:
    """Tests for `Document` model"""

    def test_create_document_successful(self, create_about) -> None:
        """Test creating `Document` objects is successful"""
        about = create_about()
        pdf = SimpleUploadedFile("resume.pdf", b"content")
        picture = SimpleUploadedFile("certificate.png", b"content")
        document1 = Document.objects.create(name="CV", parent=about, document=pdf)
        document2 = Document.objects.create(
            name="Certificate", parent=about, document=picture
        )

        documents = Document.objects.all()

        assert document1 in documents
        assert document2 in documents

    def test_document_str(self, create_document) -> None:
        """Test `Document` object string representation"""
        document = create_document(name="My document")

        assert str(document) == document.name

    def test_extension(self, create_about) -> None:
        """Test `extension` function returns file extension"""
        filename = "document.pdf"
        file_extension = filename.split(".")[-1]
        pdf = SimpleUploadedFile(filename, b"content")
        document = Document.objects.create(
            name="My document", parent=create_about(), document=pdf
        )

        assert document.extension() == file_extension


class ContactsModelTests:
    """Tests for `Contacts` model"""

    def test_create_contacts_successful(self, create_contacts) -> None:
        """Test creating `Contacts` objects is successful"""
        contacts1 = create_contacts()
        contacts2 = create_contacts()

        contacts = Contacts.objects.all()

        assert contacts1 in contacts
        assert contacts2 in contacts

    def test_contacts_str(self, create_contacts) -> None:
        """Test `Contacts` object string representation"""
        contacts = create_contacts(title="Title Title")

        assert str(contacts) == contacts.title

    def test_create_contacts_published_fails(self, create_contacts) -> None:
        """Test creating more than one published contacts raises ValidationError"""
        with pytest.raises(ValidationError):
            create_contacts(published=True)
            create_contacts(published=True)


class LinkModelTests:
    """Tests for `Link` model"""

    def test_create_link_successful(self, create_contacts, create_link) -> None:
        """Test creating `Link` objects is successful"""
        contacts = create_contacts()
        link1 = create_link(parent=contacts)
        link2 = create_link(parent=contacts)

        links = Link.objects.all()

        assert link1 in links
        assert link2 in links

    def test_link_str(self, create_link) -> None:
        """Test `Link` object string representation"""
        link = create_link(name="My Link")

        assert str(link) == link.name
