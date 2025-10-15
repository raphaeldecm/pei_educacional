from django.shortcuts import redirect


class GroupRedirectMiddleware:
    """
    Middleware para redirecionar o usuário após o login com base no grupo.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path in ("/users/list/",):
            if (
                request.user.groups.filter(name="Collaborator").exists()
                or request.user.groups.filter(name="Pedagogue").exists()
            ):
                return redirect("academics:dashboard")

        return self.get_response(request)
