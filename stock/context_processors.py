from stock.models import Alerte


def alertes_non_lues(request):
    if request.user.is_authenticated:
        count = Alerte.objects.filter(is_read=False).count()
        return {'alertes_count': count}
    return {'alertes_count': 0}
