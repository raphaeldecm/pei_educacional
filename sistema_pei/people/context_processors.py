from sistema_pei.people.models import AlertaGlobal, Notification
from django.utils import timezone


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

def alertas_globais_ativos(request):
    agora = timezone.now()
    alertas = AlertaGlobal.objects.filter(data_inicio__lte=agora, data_fim__gte=agora)
    COR_MAP = AlertaGlobal.COR_MAP

    alertas_com_classes = []
    for alerta in alertas:
        cores = COR_MAP.get(alerta.cor_base, {})
        alertas_com_classes.append({
            'mensagem': alerta.mensagem,
            'bg_class': cores.get('bg', 'bg-gray-100'),
            'text_class': cores.get('text', 'text-gray-800'),
            'border_class': cores.get('border', 'border-gray-300'),
        })

    return {
        'alertas_globais_ativos': alertas_com_classes,
    }
