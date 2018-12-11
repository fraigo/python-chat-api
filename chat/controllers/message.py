import calendar
import time
import sys
import datetime
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.forms.models import model_to_dict
from chat.models import Message , Sender, User


def createSender(email):
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
            name = email
            imageUrl = ''
        sender = Sender(email=email, name=name, imageUrl=imageUrl)
        sender.save()
    return sender

def createMessage(user, to, message):
    try:
        sender = Sender.objects.get(email=user)
    except:
        error = {
            "message" : "Invalid sender"
        }
        return error
    try:
        recipient = Sender.objects.get(email=to)
    except:
        error = {
            "message" : "Invalid recipient"
        }
        return error
    message = Message(
        sender=sender, 
        recipient=recipient,
        message=message,
        timestamp=datetime.datetime.now()
        )
    message.save()
    return message

def push(request,user):
    to = request.GET.get('to')
    message = request.GET.get('message')
    createSender(user)
    createSender(to)
    try:
        message = createMessage( user, to, message)
        data = model_to_dict(message)
        return JsonResponse(data)
    except Exception as e:
        e_type, e_obj, e_tb = sys.exc_info()
        error = {
            "message" : "Error creating message: %s (%d)" % ( str(e) , e_tb.tb_lineno )
        }
        return JsonResponse(error, status=400)
    

def get(request, user, rec = None):
    try:
        if rec:
            messages = Message.objects.filter( Q(sender__email=user) | Q(recipient__email=user) , Q(sender__email=rec) | Q(recipient__email=rec) )
        else:
            messages = Message.objects.filter( Q(sender__email=user) | Q(recipient__email=user) )
        data = []
        for msg in messages:
            data.append({
                "from" : msg.sender.email,
                "to" : msg.recipient.email,
                "message" : msg.message,
                "visible" : msg.visible,
                "timestamp" : int(msg.timestamp.timestamp())
            })
        return JsonResponse(data, safe=False)
    except Exception as e:
        e_type, e_obj, e_tb = sys.exc_info()
        error = {
            "message" : "Error creating message: %s (%d)" % ( str(e) , e_tb.tb_lineno )
        }
        return JsonResponse(error, status=400)

def senders(request, user):
    try:
        messages = Message.objects.filter( Q(sender__email=user) | Q(recipient__email=user) )
        senders1 = messages.values("sender").distinct()
        senders2 = messages.values("recipient").distinct()
        data = []
        for senderid in senders1:
            sender = Sender.objects.get(pk=senderid["sender"])
            if sender.email != user and sender not in data:
                data.append({
                    "name" : sender.name,
                    "email" : sender.email,
                    "id" : sender.id,
                    "imageUrl" : sender.imageUrl,
                })
        for senderid in senders2:
            sender = Sender.objects.get(pk=senderid["recipient"])
            if sender.email != user and sender not in data:
                data.append({
                    "name" : sender.name,
                    "email" : sender.email,
                    "id" : sender.id,
                    "imageUrl" : sender.imageUrl,
                })
        return JsonResponse(data, safe=False)
    except Exception as e:
        e_type, e_obj, e_tb = sys.exc_info()
        error = {
            "message" : "Error creating message: %s (%d)" % ( str(e) , e_tb.tb_lineno )
        }
        return JsonResponse(error, status=400)

