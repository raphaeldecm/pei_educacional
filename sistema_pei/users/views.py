from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django_filters.views import FilterView
from django.urls import reverse_lazy

from sistema_pei.core import constants
from sistema_pei.core.mixins import TitleViewMixin
from sistema_pei.users.models import User
from .filters import UserFilter

class UserDetailView(LoginRequiredMixin, TitleViewMixin, SuccessMessageMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"
    title = _("User Details")


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name", "email", "sector", "groups"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return reverse("users:detail", kwargs={"pk": self.object.pk})

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


class UsersManageAccess(
    LoginRequiredMixin,
    TitleViewMixin,
    SuccessMessageMixin,
    FilterView,
    ListView,
):
    template_name = "users/user_list.html"
    model = User
    context_object_name = "users"
    title = _("Manage Users Access")
    paginate_by = constants.DEFAULT_PAGE_SIZE
    filterset_class = UserFilter
    ordering = ["name"]
    queryset = User.objects.all().exclude(is_superuser=True).exclude(name="")

class UserManagerUpdate(
    LoginRequiredMixin,
    TitleViewMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = User
    fields = ["name", "email", "sector", "groups", "is_active"]
    success_message = _("Information successfully updated")
    title = _("User Update")
    form_class = forms.

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse("users:detail", kwargs={"pk": self.object.pk})
