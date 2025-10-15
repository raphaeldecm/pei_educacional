from django.contrib.auth.mixins import UserPassesTestMixin


class TeacherPermission(UserPassesTestMixin):
    """ "Mixin that checks if the user is a teacher"""

    def test_func(self):
        return self.request.user.groups.filter(name="Teacher").exists()


class CoordinatorPermission(UserPassesTestMixin):
    """ "Mixin that checks if the user is a coordinator"""

    def test_func(self):
        return self.request.user.groups.filter(name="Coordinator").exists()


class CollaboratorOrCoordinatorPermission(UserPassesTestMixin):
    """ "Mixin that checks if the user is a assistant or coordinator"""

    def test_func(self):
        return (
            self.request.user.groups.filter(
                name="Collaborator",
            ).exists()
            or self.request.user.groups.filter(
                name="Coordinator",
            ).exists()
        )


class AnyGroupPermission(UserPassesTestMixin):
    """ "Mixin that checks if the user is a assistant or coordinator"""

    def test_func(self):
        return (
            self.request.user.groups.filter(
                name="Assistant",
            ).exists()
            or self.request.user.groups.filter(
                name="Coordinator",
            ).exists()
            or self.request.user.groups.filter(
                name="Teacher",
            ).exists()
        )


class DontBeTeacherPermission(UserPassesTestMixin):
    """Mixin that checks if user is not teacher"""

    def test_func(self):
        return not self.request.user.groups.filter(
            name="Teacher",
        ).exists()
