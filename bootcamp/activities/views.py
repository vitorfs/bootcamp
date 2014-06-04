from django.shortcuts import render
from bootcamp.activities.models import Notification

def notifications(request):
    notifications = Notification.objects.all()
    return render(request, 'activities/notifications.html', {'notifications': notifications})