import uuid
import os
import re
from typing import Iterator, Callable
import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.transaction import TransactionManagementError
from django.conf import settings
from django.urls import reverse

from core.models import Project, About, Document, Contacts, Link


def sample_project(order: int, **params) -> Project:
    """Creates and returns `Project` object with default parameters"""
    picture = SimpleUploadedFile(
        f"{params.pop('filename', 'testfile')}.jpeg", b"file_content"
    )
    defaults = {
        "title": "My project",
        "source_link": f"https://github.com/ClassicWannabe/{uuid.uuid4()}",
        "demo_link": f"https://django-react-music-app.herokuapp.com/{uuid.uuid4()}",
        "picture": picture,
        "grid_size": 6,
        "order": order,
    }
    defaults.update(params)

    return Project.objects.create(**defaults)


def sample_about(**params) -> About:
    """Creates and returns `About` object with default parameters"""
    photo = SimpleUploadedFile(
        f"{params.pop('filename', 'testfile')}.jpeg", b"file_content"
    )
    defaults = {
        "title": "My title",
        "photo": photo,
        "content": "My awesome content",
    }
    defaults.update(params)

    return About.objects.create(**defaults)


def sample_document(**params) -> Document:
    """Creates and returns `Document` object with default parameters"""
    try:
        order = Document.objects.all().order_by("-order")[0].order
    except:
        order = 0
        
    cv = SimpleUploadedFile(
        f"{params.pop('filename', 'testfile')}.pdf", b"file_content"
    )
    defaults = {
        "name": "CV",
        "document": cv,
        "parent": sample_about(),
        "order": order + 1,
    }
    defaults.update(params)

    return Document.objects.create(**defaults)


def sample_contacts(**params) -> Contacts:
    """Creates and returns `Contacts` object with default parameters"""
    defaults = {
        "title": "My contacts",
        "content": "My content",
        "email": "ruslaneleusinov@gmail.com",
    }
    defaults.update(params)

    return Contacts.objects.create(**defaults)


def sample_link(**params) -> Link:
    """Creates and returns `Link` object with default parameters"""
    try:
        order = Link.objects.all().order_by("-order")[0].order
    except:
        order = 0
    defaults = {
        "name": "new link",
        "url": "example.com",
        "parent": sample_contacts(),
        "order": order + 1,
    }
    defaults.update(params)

    return Link.objects.create(**defaults)


def purge_files(dir: str, pattern: str) -> None:
    """Delete files from directory that match the pattern"""
    dir = settings.BASE_DIR / dir
    for f in os.listdir(dir):
        if re.search(pattern, f):
            os.remove(os.path.join(dir, f))


@pytest.fixture
def create_project() -> Iterator[Callable]:
    """
    Fixture that yields function for creating `Project` object
    then deletes all `Project` instances to trigger `post_delete` signal
    """

    yield sample_project

    try:
        Project.objects.all().delete()
    except TransactionManagementError:
        purge_files("media_root/projects", r"^testfile.*\.(jpeg|jpg|png|pdf)")


@pytest.fixture
def create_about() -> Iterator[Callable]:
    """
    Fixture that yields function for creating `About` object
    """

    yield sample_about

    purge_files("media_root/about", r"^testfile.*\.(jpeg|jpg|png|pdf)")


@pytest.fixture
def create_document() -> Iterator[Callable]:
    """
    Fixture that yields function for creating `Document` object
    """

    yield sample_document

    purge_files("media_root/about", r"^testfile.*\.(jpeg|jpg|png|pdf)")


@pytest.fixture
def create_contacts() -> Iterator[Callable]:
    """
    Fixture that yields function for creating `Contacts` object
    """

    yield sample_contacts


@pytest.fixture
def create_link() -> Iterator[Callable]:
    """
    Fixture that yields function for creating `Link` object
    """

    yield sample_link


@pytest.fixture
def about_url() -> str:
    """Fixture that returns URL for the about page"""
    return reverse("core:about")


@pytest.fixture
def project_url() -> str:
    """Fixture that returns URL for the project list page"""
    return reverse("core:projects")


@pytest.fixture
def contacts_url() -> str:
    """Fixture that returns URL for the contacts page"""
    return reverse("core:contacts")
