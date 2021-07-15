from django.http import Http404
from django.utils.translation import gettext as _


class GetPublishedPageMixin:
    """
    Mixin that replaces or adds `get_object` method of the class
    """

    def get_object(self, queryset=None):
        """
        Return the object the view is displaying.
        """
        if queryset is None:
            queryset = self.get_queryset().filter(published=True)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj
