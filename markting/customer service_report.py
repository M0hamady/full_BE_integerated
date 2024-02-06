import os
import sys
import django
from django.utils import timezone

# Adjust the path to the Django project's settings.py accordingly
sys.path.append('/home/M0hamady/supportconstruction')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supportconstruction.settings')
django.setup()
from client.models import ClientAction
from datetime import datetime
from project.slck import send_slack_notification

def get_today_reports():
    today = datetime.today()
    today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    today_end = timezone.make_aware(datetime.combine(today, datetime.max.time()))
    actions = ClientAction.objects.filter(created_date__range=(today_start, today_end), is_reported =False )
    return actions

def send_report_notification():
    client_actions = get_today_reports()

    for action in client_actions:
        client = action.client
        action_info = action.action
        notes = action.notes
        action.is_reported = True
        action.save()

        message = f"Client: {client}\nAction: {action_info}\nNotes: {notes}"

        send_slack_notification("#customer-service-notes-and-actions", message)

send_report_notification()