from django.http import HttpResponse
from django.http import JsonResponse
from django.forms.models import model_to_dict
from chat.models import User, Message
from chat.controllers import message
from chat.services import echo
from chat import errors


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
        echo_user = echo.user()
        echo_email = echo_user['email']
        message_content = echo.welcome(user)
        try:
            Message.objects.get(
                sender__email=echo_email,
                recipient__email=user.email,
                message=message_content
                )
        except:
            message.createSender(echo_email, echo_user['name'])
            message.createSender(user.email, user.name)
            message.createMessage(echo_email, user.email, message_content)
        return get(request, user.email)
    except:
        error = errors.json('Error registering user')
        return JsonResponse(error, status=400)


def get(request, user):
    try:
        user = User.objects.get(email=user)
        data = {
            "name": user.name,
            "email": user.email,
            "imageUrl": user.imageUrl,
            "contacts": message.senderData(user.email)
        }
        return JsonResponse(data)
    except:
        return HttpResponse(status=404)
