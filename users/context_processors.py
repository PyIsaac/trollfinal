
from users.models import Credit
from django.contrib.auth.models import AnonymousUser

def has_scoreback(request):
    user = request.user
    if not isinstance(user, AnonymousUser):
        try:
            credit = Credit.objects.get(user=user)
            return {'has_scoreback': credit.scoreback}
        except Credit.DoesNotExist:
            return {'has_scoreback': False}


from users.models import Credit
from django.contrib.auth.models import AnonymousUser

def has_scoreback(request):
    user = request.user
    if not isinstance(user, AnonymousUser):
        try:
            credit = Credit.objects.get(user=user)
            return {'has_scoreback': credit.scoreback}
        except Credit.DoesNotExist:
            return {'has_scoreback': False}


    return {'has_scoreback': False}