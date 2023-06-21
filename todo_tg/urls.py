from django.views.decorators.csrf import csrf_exempt
from django_telegrambot.apps import process_update

urlpatterns = [
    path('telegram-bot/', csrf_exempt(process_update)),
]