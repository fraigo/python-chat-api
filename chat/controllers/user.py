from django.http import HttpResponse
from chat.models import User

def register(request,user):
    user = User(
        email=user, 
        name=request.GET.get('name', user),
        imageUrl=request.GET.get('imageUrl', '')
        )
    user.save()
    return HttpResponse(user)

def get(request):
    return []