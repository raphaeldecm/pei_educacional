import django_filters
from django.db.models import Q
from django.utils.timezone import now,timedelta
from django.db.models.functions import Lower

from sistema_pei.academics.models import Course

from .models import Campus
from .models import Student
from .models import Teacher


class TeacherFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label="Nome")
    email = django_filters.CharFilter(lookup_expr="icontains", label="E-mail")
    campus = django_filters.ModelChoiceFilter(
        queryset=Campus.objects.all(),
        label="Campus",
    )
    code = django_filters.CharFilter(lookup_expr="icontains", label="Matrícula")

    class Meta:
        model = Teacher
        fields = ["name", "email", "campus", "code"]


class StudentFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="multi_field_search", label="Search")
    course = django_filters.ModelChoiceFilter(
        queryset=Course.objects.order_by("name", "period"),
        label="Curso",
    )
    
    STATUS_CHOICES = (
        ("RECENTE","Recente"),
        ("REGULAR","Regular"),
        ("ANTIGA","Antiga"),
        ("SEM_SINCRONIZACAO","Sem sincronização")
    )
    
    sync_status = django_filters.ChoiceFilter(
        method = 'get_student_by_sync_status',
        choices = STATUS_CHOICES
    )

    class Meta:
        model = Student
        fields = ["course"]

    def multi_field_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(registration__icontains=value),
        )

    def get_student_by_sync_status(self,quaryset,name,value):
        """
            filtra os discentes com base no seus status de sicronização
        """
        
        filter_dates_values = {
            'RECENTE' : [now() - timedelta(days=30),now()],
            'REGULAR' :[now() - timedelta(days=60),now()-timedelta(days=30)],
            "ANTIGA":[now()-timedelta(days=7305),now()-timedelta(days=60)]
        }
        
        if value == 'SEM_SINCRONIZACAO':
            return quaryset.all().exclude(enrollment__last_synced_at__isnull=False)

        #retorna os discentes que tem suas datas de sicronização no range do filtro
        return quaryset.filter(enrollment__last_synced_at__range = filter_dates_values.get(value,None))
         