from typing import Dict

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.filters import RelatedFieldListFilter
from django.contrib.admin.options import IncorrectLookupParameters
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS, get_language
from django.db.models import Model, QuerySet
from django.db.models.fields.related import ForeignKey
from django.http import HttpRequest
from django.urls import reverse


class AutocompleteFilter(RelatedFieldListFilter):
    template = "common/admin/autocomplete_filter.html"
    url_name = "%s:autocomplete"
    parameter_name = None

    def __init__(
        self, field: ForeignKey, request: HttpRequest, params: Dict[str, str], model: Model, model_admin: admin.ModelAdmin, field_path: str
    ):
        self.parameter_name = self.parameter_name or field_path
        super().__init__(field, request, params, model, model_admin, field_path)
        self.admin_site = model_admin.admin_site
        self.value = params.pop(self.parameter_name, None)
        self.value_title = field.related_model.objects.get(pk=self.value) if self.value else None
        # Based on Django's own AutocompleteMixin: https://github.com/django/django/blob/stable/3.2.x/django/contrib/admin/widgets.py#L405
        self.autocomplete_configuration = {
            "data-ajax--cache": "true",
            "data-ajax--delay": 250,
            "data-ajax--type": "GET",
            "data-ajax--url": self.get_url(),
            "data-app-label": field.model._meta.app_label,
            "data-model-name": field.model._meta.model_name,
            "data-field-name": field.name,
            "data-theme": "admin-autocomplete",
            "data-allow-clear": "true",
            "data-placeholder": "",  # Allows clearing of the input.
            "lang": SELECT2_TRANSLATIONS.get(get_language()),
        }

    def get_url(self):
        return reverse(self.url_name % self.admin_site.name)

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:
        try:
            queryset = super().queryset(request, queryset)
        except IncorrectLookupParameters as e:
            # Ignore exception for providing empty query parameter and just return unfiltered queryset.
            if "is not a valid UUID." in str(e):
                pass
        if self.value:
            queryset = queryset.filter(**{self.parameter_name: self.value})
        return queryset


class AutocompleteAdminMedia:
    """
    A list of javascript and css files which are needed to render a select2 autocomplete widget.
    This list is based on Django's own autocomplete widget and reuses the files bundled with the framework.
    https://github.com/django/django/blob/stable/3.2.x/django/contrib/admin/widgets.py#L450
    """

    i18n_name = SELECT2_TRANSLATIONS.get(get_language())
    i18n_file = ("admin/js/vendor/select2/i18n/%s.js" % i18n_name,) if i18n_name else ()
    extra = "" if settings.DEBUG else ".min"

    js = (
        (
            "admin/js/vendor/jquery/jquery%s.js" % extra,
            "admin/js/vendor/select2/select2.full%s.js" % extra,
        )
        + i18n_file
        + (
            "admin/js/jquery.init.js",
            "admin/js/autocomplete.js",
            # Unlike all previous entries, this is a custom JS file from this project rather than a Django one!
            "common/admin/autocompleteFilter.js",
        )
    )
    css = {
        "screen": (
            "admin/css/vendor/select2/select2%s.css" % extra,
            "admin/css/autocomplete.css",
        )
    }
