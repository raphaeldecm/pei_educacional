import django_filters
from django.db.models import Q
from sistema_pei.academics.models import Enrollment, Offer

class OfferFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_search', label='Search')
    
    class Meta:
        model = Offer
        fields = {
            'teacher': ['exact'],
            'subject': ['exact'],
        }

    def filter_by_search(self, queryset, name, value):
        return queryset.filter(
            Q(subject__name__icontains=value) |
            Q(teacher__name__icontains=value)
        )
        
class EnrollmentFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name='student__name', lookup_expr='icontains', label='Search')

    class Meta:
        model = Enrollment
        fields = []
