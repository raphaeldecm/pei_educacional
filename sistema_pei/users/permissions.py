from django.contrib.auth.mixins import UserPassesTestMixin


class TeacherPermission(UserPassesTestMixin):
    """ "Mixin that checks if the user is a teacher"""

    def test_func(self):
        return self.request.user.groups.filter(name="Teacher").exists()


class CoordinatorPermission(UserPassesTestMixin):
    """ "Mixin that checks if the user is a coordinator"""

    def test_func(self):
        return self.request.user.groups.filter(name="Coordinator").exists()


class AssistentOrCoordinatorPermission(UserPassesTestMixin):
    """ "Mixin that checks if the user is a assistant or coordinator"""

    def test_func(self):
        return (
            self.request.user.groups.filter(
                name="Assistant",
            ).exists()
            or self.request.user.groups.filter(
                name="Coordinator",
            ).exists()
        )
