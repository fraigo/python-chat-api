from django.http import HttpResponse
from django.http import JsonResponse
from django.forms.models import model_to_dict
from chat.models import User
from chat.controllers import message


def register(request, user):
    try:
        user = User.objects.get(email=user)
        user.name = request.GET.get('name', user.name)
        user.imageUrl = request.GET.get('imageUrl', user.imageUrl)
        user.save()
    except:
        user = User(
            email=user,
            name=request.GET.get('name', user),
            imageUrl=request.GET.get('imageUrl', '')
        )
    try:
        user.save()
        return get(request, user.email)
    except:
        error = {
            "message" : "Error"
        }
        return JsonResponse(error, status=400)
    

def get(request, user):
    try:
        user = User.objects.get(email=user)
        data = {
            "name" : user.name,
            "email" : user.email,
            "imageUrl" : user.imageUrl,
            "contacts" : message.senderData(user.email)
        }
        return JsonResponse(data)
    except:
        return HttpResponse(status=404)
