from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.db.models.functions import Lower
from django.shortcuts import redirect


class TitleViewMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context


class ProtectedErrorMessageMixin:
    protected_warning_message = ""

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.warning(self.request, self.protected_warning_message)
            return redirect(self.request.headers.get("referer"))


class OptionalUserFieldMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "user" in self.fields:
            self.fields["user"].required = False


class Icontains_with_unaccentMinxin:
    """adiciona um filtro de busca ignorando acentos"""

    def search_icontains(self, query, name, value):
        """
        Método que filtra o queryset com base no valor de busca
        """
        return query.filter(**{f"{name}__unaccent__icontains": value}).order_by(
            Lower(name)
        )
