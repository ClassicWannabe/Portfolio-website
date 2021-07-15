import os

from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Project(models.Model):
    """Model for project objects"""

    title = models.CharField(_("project title"), max_length=50)
    description = models.TextField(_("description"), blank=True)
    source_link = models.URLField(_("source code link"), unique=True)
    demo_link = models.URLField(_("link to demo"), unique=True)
    picture = models.ImageField(_("screenshot"), upload_to="projects")
    grid_size = models.PositiveSmallIntegerField(
        _("grid size on desktop page"),
        validators=[MinValueValidator(1), MaxValueValidator(12)],
    )
    order = models.PositiveSmallIntegerField(_("order"), unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order"]


class About(models.Model):
    """Model for about page"""

    title = models.CharField(_("page title"), max_length=100)
    photo = models.ImageField(_("my photo"), upload_to="about")
    content = models.TextField(_("page content"))
    published = models.BooleanField(_("published"), default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Checks whether there is an existing published About object
        and raises ValidationError if true
        """
        published_pages = self._meta.model.objects.filter(published=True)
        if (
            self.published
            and published_pages.exists()
            and published_pages[0].id != self.id
        ):
            raise ValidationError("There must be only one published About object")
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("About page")
        verbose_name_plural = _("About page")


class Document(models.Model):
    """Model for files on about page"""

    parent = models.ForeignKey(
        "About", related_name="documents", on_delete=models.CASCADE
    )
    name = models.CharField(_("document name"), max_length=50)
    document = models.FileField(_("document"), upload_to="about")

    def __str__(self):
        return self.name

    def extension(self):
        """Returns document extension"""
        _, extension = os.path.splitext(self.document.name)
        return extension[1:]


class Contacts(models.Model):
    """Model for contacts page"""

    title = models.CharField(_("page title"), max_length=100)
    content = models.TextField(_("page content"))
    email = models.EmailField(_("email to copy"))
    published = models.BooleanField(_("published"), default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Checks whether there is an existing published Contacts object
        and raises ValidationError if true
        """
        published_pages = self._meta.model.objects.filter(published=True)
        if (
            self.published
            and published_pages.exists()
            and published_pages[0].id != self.id
        ):
            raise ValidationError("There must be only one published Contacts object")
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Contacts page")
        verbose_name_plural = _("Contacts page")


class Link(models.Model):
    """Model for links on contacts page"""

    name = models.CharField(_("link name"), max_length=100)
    url = models.URLField(_("URL"))
    parent = models.ForeignKey(
        "Contacts", related_name="links", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


@receiver(models.signals.post_delete, sender=Project)
def auto_delete_picture_on_delete(sender, instance, **kwargs):
    """
    Deletes picture from filesystem
    when corresponding `Project` object is deleted.
    """
    if instance.picture:
        if os.path.isfile(instance.picture.path):
            os.remove(instance.picture.path)


@receiver(models.signals.pre_save, sender=Project)
def auto_delete_picture_on_change(sender, instance, **kwargs):
    """
    Deletes old picture from filesystem
    when corresponding `Project` object is updated
    with new picture.
    """
    if not instance.pk:
        return False

    try:
        old_picture = Project.objects.get(pk=instance.pk).picture
    except Project.DoesNotExist:
        return False

    new_picture = instance.picture
    if not old_picture == new_picture:
        if os.path.isfile(old_picture.path):
            os.remove(old_picture.path)
