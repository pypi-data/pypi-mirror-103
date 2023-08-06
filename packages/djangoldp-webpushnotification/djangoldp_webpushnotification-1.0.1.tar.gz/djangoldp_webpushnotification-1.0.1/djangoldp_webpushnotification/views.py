import json

from django.conf import settings
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from webpush import send_user_notification

from djangoldp_account.models import LDPUser
from djangoldp_webpushnotification.models import VAPIDKeyset


@require_POST
@csrf_exempt
def send_push(request):
    try:
        body = request.body
        data = json.loads(body)

        if "head" not in data or "body" not in data or "id" not in data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})

        user_id = data["id"]
        user = get_object_or_404(LDPUser, pk=user_id)
        payload = {"head": data["head"], "body": data["body"]}
        vapid_key = VAPIDKeyset.objects.first()
        settings.WEBPUSH_SETTINGS['VAPID_PUBLIC_KEY'] = vapid_key.public_key
        settings.WEBPUSH_SETTINGS['VAPID_PRIVATE_KEY'] = vapid_key.private_key.tobytes().decode()

        send_user_notification(user=user, payload=payload, ttl=1000)

        return JsonResponse(status=200, data={"message": "Web push successful"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})
