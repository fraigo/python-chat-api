import calendar
import time
import datetime
import importlib
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.forms.models import model_to_dict
from chat.models import Message, Sender, User
from chat import errors


def createSender(email, name=None):
    if not name:
        name = email
    try:
        sender = Sender.objects.get(email=email)
        try:
            tmpUser = User.objects.get(email=email)
            sender.name = tmpUser.name
            sender.imageUrl = tmpUser.imageUrl
            sender.save()
        except:
            pass
    except:
        try:
            toUser = User.objects.get(email=email)
            name = toUser.name
            imageUrl = toUser.imageUrl
        except:
            imageUrl = ''
        sender = Sender(email=email, name=name, imageUrl=imageUrl)
        sender.save()
    return sender


def createMessage(user, to, message):
    try:
        sender = Sender.objects.get(email=user)
    except:
        raise ValueError('Invalid Sender %s' % user)
    try:
        recipient = Sender.objects.get(email=to)
    except:
        raise ValueError('Invalid Recipient %s' % to)
    message = Message(
        sender=sender,
        recipient=recipient,
        message=message,
        timestamp=datetime.datetime.now()
        )
    message.save()
    return message


def push(request, user):
    to = request.GET.get('to')
    msg = request.GET.get('message')
    createSender(user)
    createSender(to)
    try:
        message = createMessage(user, to, msg)
        data = model_to_dict(message)
        service, host = to.split("@")
        if host == "imessenger.com":
            try:
                svc = importlib.import_module('chat.services.%s' % service)
                receiver = Sender.objects.get(email=user)
                answer = svc.message(receiver, msg)
                createMessage(to, receiver.email, answer)
                data["service"] = service
            except:
                error = errors.json('Error in service %s' % service)
                return JsonResponse(error, status=400)
        return JsonResponse(data)
    except Exception as e:
        error = errors.json('Error creating message')
        return JsonResponse(error, status=400)


def get(request, user, rec=None):
    try:
        if rec:
            messages = Message.objects.filter(
                Q(sender__email=user) | Q(recipient__email=user),
                Q(sender__email=rec) | Q(recipient__email=rec)
                )
        else:
            messages = Message.objects.filter(
                Q(sender__email=user) | Q(recipient__email=user)
                )
        data = []
        for msg in messages:
            data.append({
                "from": msg.sender.email,
                "to": msg.recipient.email,
                "message": msg.message,
                "visible": msg.visible,
                "timestamp": int(msg.timestamp.timestamp())
            })
        return JsonResponse(data, safe=False)
    except Exception as e:
        error = errors.json('Error getting messages')
        return JsonResponse(error, status=400)


def senderData(user):
    messages = Message.objects.filter(
        Q(sender__email=user) | Q(recipient__email=user)
        ).order_by('-timestamp')
    senders1 = messages.values("sender").distinct()
    senders2 = messages.values("recipient").distinct()
    data = []
    emails = []
    for senderid in senders1:
        sender = Sender.objects.get(pk=senderid["sender"])
        if sender.email != user and sender.email not in emails:
            emails.append(sender.email)
            data.append({
                "name": sender.name,
                "email": sender.email,
                "id": sender.id,
                "imageUrl": sender.imageUrl,
            })
    for senderid in senders2:
        sender = Sender.objects.get(pk=senderid["recipient"])
        if sender.email != user and sender.email not in emails:
            emails.append(sender.email)
            data.append({
                "name": sender.name,
                "email": sender.email,
                "id": sender.id,
                "imageUrl": sender.imageUrl,
            })
    return data


def senders(request, user):
    try:
        data = senderData(user)
        return JsonResponse(data, safe=False)
    except:
        error = errors.json('Error getting servers')
        return JsonResponse(error, status=400)
