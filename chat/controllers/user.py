from django.http import HttpResponse
from django.http import JsonResponse
from django.forms.models import model_to_dict
from chat.models import User

def register(request,user):
    try:
        user = User.objects.get(email=user)
        user.name = request.GET.get('name', user.name)
        user.imageUrl = request.GET.get('imageUrl', user.imageUrl)
        user.save
    except:
        user = User(
            email=user, 
            name=request.GET.get('name', user),
            imageUrl=request.GET.get('imageUrl', '')
            )
    try:
        user.save()
        data = model_to_dict(user)
        return JsonResponse(data)
    except:
        error = {
            "message" : "Error"
        }
        return JsonResponse(error, status=400)
    

def get(request, user):
    try:
        user = User.objects.get(email=user)
        data = model_to_dict(user)
        return JsonResponse(data)
    except:
        return HttpResponse(status=404)
