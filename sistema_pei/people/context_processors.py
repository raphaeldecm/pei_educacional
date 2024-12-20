from sistema_pei.people.models import Notification


def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(
            user=request.user, viewed=False
        ).order_by("-created_at")
    else:
        notifications = Notification.objects.none()

    return {
        "notifications": notifications,
    }
