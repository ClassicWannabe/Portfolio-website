from django.contrib import admin

from .models import Project, About, Document, Contacts, Link, Carousel


class DocumentInline(admin.StackedInline):
    model = Document
    extra = 1


class LinkInline(admin.StackedInline):
    model = Link
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "grid_size")
    list_editable = ("order", "grid_size")


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("title", "published")
    inlines = [DocumentInline]


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ("title", "published")
    inlines = [LinkInline]


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ("__str__", "published", "order")
    list_editable = ("published", "order")
