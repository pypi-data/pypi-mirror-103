import json

from django.conf import settings
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from djangoldp_account.models import LDPUser
from webpush import send_user_notification

from djangoldp_webpushnotification.models import VAPIDKeyset


@require_POST
@csrf_exempt
def send_push(request):
    try:
        body = request.body
        data = json.loads(body)
        if "head" not in data or "body" not in data or "id" not in data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})
    except TypeError:
        return JsonResponse(status=400, data={"message": "Invalid data format"})

    user = get_object_or_404(LDPUser, pk=data["id"])

    vapid_key = VAPIDKeyset.objects.first()
    if not vapid_key:
        return JsonResponse(status=400, data={"message": "No VAPID key configured"})

    settings.WEBPUSH_SETTINGS["VAPID_PUBLIC_KEY"] = vapid_key.public_key
    settings.WEBPUSH_SETTINGS["VAPID_PRIVATE_KEY"] = vapid_key.private_key.decode()

    if "VAPID_ADMIN_EMAIL" not in settings.WEBPUSH_SETTINGS:
        return JsonResponse(
            status=400, data={"message": "No VAPID admin email configured"}
        )

    payload = {"head": data["head"], "body": data["body"]}
    send_user_notification(user=user, payload=payload, ttl=1000)

    return JsonResponse(status=200, data={"message": "Web push successful"})
